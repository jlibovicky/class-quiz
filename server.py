#!/usr/bin/env python3

from typing import Tuple
import argparse
import json
import datetime
from multiprocessing import Manager
import os
import subprocess

from apscheduler.schedulers.background import BackgroundScheduler
import flask
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from markdown import markdown

from quiz import parse_markdown_quiz


def html(text: str) -> str:
    return markdown(text).removeprefix("<p>").removesuffix("</p>")


app = Flask(__name__, template_folder='template')
app.jinja_env.globals.update(html=html)
auth = HTTPBasicAuth()


CORRECT_PASSWORD = None
@auth.verify_password
def verify_password(_, password: str) -> bool:
    return password == CORRECT_PASSWORD


# Stuff that needs to be shared between processes
manager = Manager()
answer_counts = manager.dict()
last_save_timestamp = manager.Value("f", 0.0)
last_answer_timestamp = manager.Value("f", 0.0)

QUIZ_DIR = "quizzes"
quizzes = manager.dict()
failed_quizzes = manager.list()


ANSWER_COUNTS_FILE = "answer_counts.json"

def save_answer_counts() -> None:
    if last_answer_timestamp.value > last_save_timestamp.value:
        with open(ANSWER_COUNTS_FILE, "w", encoding="utf-8") as f_json:
            json.dump(answer_counts.copy(), f_json)
        last_save_timestamp.value = datetime.datetime.now().timestamp()


def load_answer_counts() -> None:
    if os.path.exists(ANSWER_COUNTS_FILE):
        with open(ANSWER_COUNTS_FILE, "r", encoding="utf-8") as f_json:
            answer_counts.update(json.load(f_json))
        last_save_timestamp.value = datetime.datetime.now().timestamp()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(save_answer_counts, "interval", seconds=60)
scheduler.start()


@app.route("/script.js")
def script():
    return flask.send_file("script.js")


@app.route("/quiz")
@app.route("/answer_stats")
@app.route("/timer")
@app.route("/")
@auth.login_required
def index() -> str:
    return flask.render_template(
        "quiz_listing.html",
        quizzes=quizzes,
        failed_quizzes=failed_quizzes)


@app.route("/quiz/<path:quiz_id>")
def quiz(quiz_id: str) -> Tuple[str, int]:
    if quiz_id not in quizzes:
        return f"Quiz '{quiz_id}' not found.", 404
    return flask.render_template(
            "student_interface.html", quiz=quizzes[quiz_id]), 200


@app.route("/quiz/<path:quiz_id>/answer/<int:question_id>/<int:answer_id>")
def answer(quiz_id: str, question_id: int, answer_id: int) -> Tuple[str, int]:
    if quiz_id not in quizzes:
        return f"Quiz '{quiz_id}' not found.", 404
    if question_id >= len(quizzes[quiz_id].questions):
        return f"Question '{question_id}' not found.", 404
    is_correct = (
        quizzes[quiz_id].questions[question_id].correct_answer == answer_id)

    cache_key = f"{quiz_id}-{question_id}-{answer_id}"
    answer_counts[cache_key] = answer_counts.get(cache_key, 0) + 1
    last_answer_timestamp.value = datetime.datetime.now().timestamp()
    return str(is_correct), 200


@app.route("/answer_stats/<path:quiz_id>")
@auth.login_required
def answers(quiz_id: str) -> Tuple[str, int]:
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
            answer_counts=quiz_specific_counts), 200


def load_quizes() -> None:
    # Hack to clear out the previously failed quizzes
    failed_quizzes[:] = []
    for file_name in os.listdir(QUIZ_DIR):
        if not file_name.endswith(".md"):
            continue
        q_id = os.path.splitext(file_name)[0]
        print(f"Loading quiz '{q_id}'")
        try:
            quizzes[q_id] = parse_markdown_quiz(
                os.path.join(args.quiz_dir, file_name))
        except ValueError as error:
            print(f"Failed to load quiz '{q_id}': {error}")
            failed_quizzes.append(q_id)


@app.route("/timer/<path:quiz_id>")
@auth.login_required
def timer(quiz_id: str) -> Tuple[str, int]:
    if quiz_id not in quizzes:
        return f"Quiz '{quiz_id}' not found.", 404
    return flask.render_template(
            "timer.html", quiz=quizzes[quiz_id], quiz_id=quiz_id), 200


@app.route("/github_update", methods=["POST"])
def github_update() -> Tuple[str, int]:
    subprocess.run(["git", "pull"], check=False)
    load_quizes()
    return ("", 200)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to listen on.")
    parser.add_argument(
        "--port", default=5000, type=int, help="Port to listen on.")
    parser.add_argument(
        "--quiz-dir", default="quizzes",
        help="Directory to load quizzes from.")
    parser.add_argument(
        "--answer-counts-file", default="answer_counts.json",
        help="File to load answer counts from")
    parser.add_argument(
        "--password", default="password",
        help="Password for teacher interface")
    args = parser.parse_args()

    CORRECT_PASSWORD = args.password
    QUIZ_DIR = args.quiz_dir
    ANSWER_COUNTS_FILE = args.answer_counts_file

    load_answer_counts()
    load_quizes()

    app.run(host=args.host, port=args.port, debug=False)
