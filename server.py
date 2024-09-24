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

from qa_session import QASession
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
last_quiz_save_timestamp = manager.Value("f", 0.0)
last_quiz_answer_timestamp = manager.Value("f", 0.0)

last_qa_save_timestamp = manager.Value("f", 0.0)
last_qa_answer_timestamp = manager.Value("f", 0.0)

QUIZ_DIR = "quizzes"
quizzes = manager.dict()
failed_quizzes = manager.list()

qa_sessions = manager.dict()


ANSWER_COUNTS_FILE = "answer_counts.json"
QA_DATA_FILE = "qa_data.json"

def save_app_state() -> None:
    if last_quiz_answer_timestamp.value > last_quiz_save_timestamp.value:
        with open(ANSWER_COUNTS_FILE, "w", encoding="utf-8") as f_json:
            json.dump(answer_counts.copy(), f_json)
        last_quiz_save_timestamp.value = datetime.datetime.now().timestamp()
    if last_qa_answer_timestamp.value > last_qa_save_timestamp.value:
        with open(QA_DATA_FILE, "w", encoding="utf-8") as f_json:
            json.dump(qa_sessions.copy(), f_json)
        last_qa_save_timestamp.value = datetime.datetime.now().timestamp()


def load_app_state() -> None:
    if os.path.exists(ANSWER_COUNTS_FILE):
        with open(ANSWER_COUNTS_FILE, "r", encoding="utf-8") as f_json:
            answer_counts.update(json.load(f_json))
        last_quiz_save_timestamp.value = datetime.datetime.now().timestamp()
    if os.path.exists(QA_DATA_FILE):
        with open(QA_DATA_FILE, "r", encoding="utf-8") as f_json:
            qa_sessions.update(json.load(f_json))
        last_qa_save_timestamp.value = datetime.datetime.now().timestamp()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(save_app_state, "interval", seconds=60)
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
        failed_quizzes=failed_quizzes,
        qa_sessions=qa_sessions)


@app.route("/quiz/<path:quiz_id>")
def quiz(quiz_id: str) -> Tuple[str, int]:
    if quiz_id not in quizzes:
        return f"Quiz '{quiz_id}' not found.", 404
    return flask.render_template(
            "quiz_assignment.html", quiz=quizzes[quiz_id]), 200


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
    last_quiz_answer_timestamp.value = datetime.datetime.now().timestamp()
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
            "index.html",
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
    quiz = quizzes[quiz_id]
    return flask.render_template(
            "timer.html",
            title=quiz.title,
            redirect_url=f"../answer_stats/{quiz_id}",
            qr_code_url=f"../quiz/{quiz_id}"), 200


@app.route("/github_update", methods=["POST"])
def github_update() -> Tuple[str, int]:
    subprocess.run(["git", "pull"], check=False)
    load_quizes()
    return ("", 200)


@app.route("/create_qa_session", methods=["POST"])
def create_qa_session() -> Tuple[str, int]:
    session_id = flask.request.form["session_id"]

    # Create a directory for a QA session
    qa_sessions[session_id] = QASession(datetime.datetime.now(), manager)

    # Redirect to the QA session timer
    return flask.redirect(f"./qa_question_timer/{session_id}?minutes=2")


@app.route("/qa_question_timer/<path:session_id>")
@auth.login_required
def qa_question_timer(session_id: str) -> Tuple[str, int]:
    if session_id not in qa_sessions:
        return f"QA session '{session_id}' not found.", 404
    session = qa_sessions[session_id] 
    return flask.render_template(
            "timer.html",
            title="Ask a question",
            redirect_url=f"../qa_voting_timer/{session_id}?minutes=2",
            qr_code_url=f"../qa_question_form/{session_id}"), 200


@app.route("/qa_question_form/<path:session_id>")
def qa_question_form(session_id: str) -> Tuple[str, int]:
    if session_id not in qa_sessions:
        return f"QA session '{session_id}' not found.", 404

    return flask.render_template("qa_question_form.html", session_id=session_id)


@app.route("/qa_ask_question", methods=["POST"])
def ask_question() -> Tuple[str, int]:
    # Get session ID and question text from the form
    session_id = flask.request.form["session_id"]
    question_text = flask.request.form["question_text"]

    # Add the question to the QA session
    qa_sessions[session_id].add_question(question_text, manager)

    return "", 200


@app.route("/qa_voting_timer/<path:session_id>")
@auth.login_required
def qa_voting_timer(session_id: str) -> Tuple[str, int]:
    if session_id not in qa_sessions:
        return f"QA session '{session_id}' not found.", 404
    session = qa_sessions[session_id] 
    session.allows_votes.set(True)
    return flask.render_template(
            "timer.html",
            title="Vote on questions",
            start_directly=True,
            redirect_url=f"../qa_results/{session_id}",
            qr_code_url=f"../qa_vote/{session_id}"), 200


@app.route("/qa_question_vote", methods=["POST"])
def qa_question_vote() -> Tuple[str, int]:
    session_id = flask.request.form["session_id"]
    question_id = int(flask.request.form["question_id"])

    if session_id not in qa_sessions:
        return f"QA session '{session_id}' not found.", 404
    if question_id >= len(qa_sessions[session_id].questions):
        return f"Question '{question_id}' not found in session '{session_id}'.", 404

    if flask.request.form["vote"] == "up":
        qa_sessions[session_id].questions[question_id].like()
    elif flask.request.form["vote"] == "down":
        qa_sessions[session_id].questions[question_id].dislike()
    else:
        return "Invalid vote.", 400

    return "", 200


@app.route("/qa_vote/<path:session_id>")
def show_questions(session_id: str) -> Tuple[str, int]:
    if session_id not in qa_sessions:
        return f"QA session '{session_id}' not found.", 404
    session = qa_sessions[session_id]
    if not session.allows_votes.get():
        # TODO do a page saying that voting is disabled
        return flask.render_template(
            "qa_voting_na.html"), 200

    return flask.render_template(
        "qa_vote.html",
        session_id=session_id,
        session=qa_sessions[session_id]), 200


@app.route("/qa_results/<path:session_id>")
def qa_results(session_id: str) -> Tuple[str, int]:
    if session_id not in qa_sessions:
        return f"QA session '{session_id}' not found.", 404
    return flask.render_template(
        "qa_results.html",
        session_id=session_id,
        session=qa_sessions[session_id]), 200


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

    load_app_state()
    load_quizes()

    app.run(host=args.host, port=args.port, debug=True)
