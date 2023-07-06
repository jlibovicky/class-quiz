#!/usr/bin/env python3

import argparse
import json
import datetime
from multiprocessing import Manager
import os

from apscheduler.schedulers.background import BackgroundScheduler
import flask
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from markdown import markdown

from quiz import parse_quiz


def md(text: str) -> str:
    return markdown(text).removeprefix("<p>").removesuffix("</p>")


app = Flask(__name__, template_folder='template')
app.jinja_env.globals.update(md=md)
auth = HTTPBasicAuth()


correct_password = None
@auth.verify_password
def verify_password(username, password):
    return password == correct_password


# Stuff that needs to be shared between processes
manager = Manager()
answer_counts = manager.dict()
last_save_timestamp = manager.Value("f", 0)
last_answer_timestamp = manager.Value("f", 0)

quizzes = {}


answer_counts_file = "answer_counts.json"

def save_answer_counts():
    global last_save_timestamp
    if last_answer_timestamp.value > last_save_timestamp.value:
        with open(answer_counts_file, "w") as f:
            json.dump(answer_counts.copy(), f)
        last_save_timestamp.value = datetime.datetime.now().timestamp()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(save_answer_counts, "interval", seconds=60)
scheduler.start()


@app.route("/script.js")
def script():
    return flask.send_file("script.js")


@app.route("/")
@app.route("/quiz")
@app.route("/answer_stats")
@auth.login_required
def hello_world():
    return flask.render_template("quiz_listing.html", quizzes=quizzes)


@app.route("/quiz/<path:quiz_id>")
def quiz(quiz_id):
    if quiz_id not in quizzes:
        return f"Quiz '{quiz_id}' not found.", 404
    return flask.render_template("student_interface.html", quiz=quizzes[quiz_id])


@app.route("/quiz/<path:quiz_id>/answer/<int:question_id>/<int:answer_id>")
def answer(quiz_id, question_id, answer_id):
    if quiz_id not in quizzes:
        return f"Quiz '{quiz_id}' not found.", 404
    if question_id >= len(quizzes[quiz_id].questions):
        return f"Question '{question_id}' not found.", 404
    is_correct = quizzes[quiz_id].questions[question_id].correct_answer == answer_id

    cache_key = f"{quiz_id}-{question_id}-{answer_id}"
    answer_counts[cache_key] = answer_counts.get(cache_key, 0) + 1
    last_answer_timestamp.value = datetime.datetime.now().timestamp()
    return str(is_correct)


@app.route("/answer_stats/<path:quiz_id>")
@auth.login_required
def answers(quiz_id):
    if quiz_id not in quizzes:
        return f"Quiz '{quiz_id}' not found.", 404

    quiz_specific_counts = {}
    for key, value in answer_counts.copy().items():
        quiz_id_, question_id, answer_id = key.split("-")
        if quiz_id_ == quiz_id:
            quiz_specific_counts[int(question_id), int(answer_id)] = value

    return flask.render_template(
            "teacher_interface.html",
            quiz=quizzes[quiz_id], quiz_id=quiz_id,
            answer_counts=quiz_specific_counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", help="Host to listen on.")
    parser.add_argument("--port", default=5000, type=int, help="Port to listen on.")
    parser.add_argument(
        "--quiz-dir", default="quizzes", help="Directory to load quizzes from.")
    parser.add_argument(
        "--answer-counts-file", default="answer_counts.json",
        help="File to load answer counts from")
    parser.add_argument(
        "--password", default="password", help="Password for teacher interface")
    args = parser.parse_args()

    correct_password = args.password
    answer_counts_file = args.answer_counts_file
    if os.path.exists(answer_counts_file):
        with open(answer_counts_file) as f:
            answer_counts.update(json.load(f))

    for file_name in os.listdir(args.quiz_dir):
        quiz_id = os.path.splitext(file_name)[0]
        quizzes[quiz_id] = parse_quiz(os.path.join(args.quiz_dir, file_name))

    app.run(host=args.host, port=args.port, debug=True)
