#!/usr/bin/env python3

import hashlib
from typing import Tuple
import argparse
import csv
import io
import json
import datetime
from multiprocessing import Manager
import os
import subprocess
import urllib.parse

from apscheduler.schedulers.background import BackgroundScheduler
import flask
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from markdown import markdown

from attendance import (
    Attendance, KeyStore, Schedule, attendance_summary, attended_lecture,
    normalize_login)
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
last_qa_action_timestamp = manager.Value("f", 0.0)

QUIZ_DIR = "quizzes"
quizzes = manager.dict()
failed_quizzes = manager.list()

qa_sessions = manager.dict()

# Key of a used one-time link -> the check-in it was used for.
attendance_records = manager.dict()
last_attendance_save_timestamp = manager.Value("f", 0.0)
last_attendance_action_timestamp = manager.Value("f", 0.0)

SCHEDULE_FILE = "schedule.csv"
ATTENDANCE_KEYS_FILE = "attendance_keys.txt"
schedule = Schedule(SCHEDULE_FILE)
key_store = KeyStore(ATTENDANCE_KEYS_FILE)


ANSWER_COUNTS_FILE = "answer_counts.json"
QA_DATA_FILE = "qa_data.json"
ATTENDANCE_FILE = "attendance.json"

def save_app_state() -> None:
    if last_quiz_answer_timestamp.value > last_quiz_save_timestamp.value:
        with open(ANSWER_COUNTS_FILE, "w", encoding="utf-8") as f_json:
            json.dump(answer_counts.copy(), f_json)
        last_quiz_save_timestamp.value = datetime.datetime.now().timestamp()
    if last_qa_action_timestamp.value > last_qa_save_timestamp.value:
        with open(QA_DATA_FILE, "w", encoding="utf-8") as f_json:
            json.dump({qa_name: session.to_json() for qa_name, session in qa_sessions.items()}, f_json)
        last_qa_save_timestamp.value = datetime.datetime.now().timestamp()
    if last_attendance_action_timestamp.value > last_attendance_save_timestamp.value:
        with open(ATTENDANCE_FILE, "w", encoding="utf-8") as f_json:
            json.dump(
                {key: record.to_json()
                 for key, record in attendance_records.items()}, f_json)
        last_attendance_save_timestamp.value = datetime.datetime.now().timestamp()


def load_app_state() -> None:
    if os.path.exists(ANSWER_COUNTS_FILE):
        with open(ANSWER_COUNTS_FILE, "r", encoding="utf-8") as f_json:
            answer_counts.update(json.load(f_json))
        last_quiz_save_timestamp.value = datetime.datetime.now().timestamp()
    if os.path.exists(QA_DATA_FILE):
        with open(QA_DATA_FILE, "r", encoding="utf-8") as f_json:
            loaded_qa_sessions = json.load(f_json)
            qa_sessions.update({
                session_id: QASession.from_json_dict(
                    session_dict, manager)
                for session_id, session_dict in loaded_qa_sessions.items()})
        last_qa_save_timestamp.value = datetime.datetime.now().timestamp()
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f_json:
            attendance_records.update({
                key: Attendance.from_json_dict(record)
                for key, record in json.load(f_json).items()})
        last_attendance_save_timestamp.value = datetime.datetime.now().timestamp()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(save_app_state, "interval", seconds=60)
scheduler.start()


# The app runs behind a proxy under a path prefix it does not know about, so
# all URLs must be relative. Never let Werkzeug make redirects absolute.
app.response_class.autocorrect_location_header = False


def relative_root() -> str:
    """Relative URL of the app root as seen from the current request."""
    return "../" * (flask.request.path.count("/") - 1) or "./"


@app.context_processor
def inject_relative_root() -> dict:
    return {"root": relative_root()}


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

    # Log that the quiz was started including the time and a MD5 hash of the IP
    # address of the client. 
    with open("quiz_open.log", "a") as f_log:
        addr_hash = hashlib.md5(flask.request.remote_addr.encode()).hexdigest()
        print(
            f"{datetime.datetime.now()} {quiz_id} {addr_hash}",
            file=f_log)

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
    schedule.reload()
    key_store.reload()
    return ("", 200)


@app.route("/create_qa_session", methods=["POST"])
def create_qa_session() -> Tuple[str, int]:
    session_id = flask.request.form["session_id"]

    # Create a directory for a QA session
    qa_sessions[session_id] = QASession(
        datetime.datetime.now().timestamp(), manager)

    last_qa_action_timestamp.value = datetime.datetime.now().timestamp()

    # Redirect to the QA session timer
    return flask.redirect(f"./qa_question_timer/{session_id}?minutes=1&seconds=30")


@app.route("/qa_question_timer/<path:session_id>")
@auth.login_required
def qa_question_timer(session_id: str) -> Tuple[str, int]:
    if session_id not in qa_sessions:
        return f"QA session '{session_id}' not found.", 404
    session = qa_sessions[session_id] 
    return flask.render_template(
            "timer.html",
            title="Ask a question",
            redirect_url=f"../qa_voting_timer/{session_id}?minutes=0&seconds=30",
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

    last_qa_action_timestamp.value = datetime.datetime.now().timestamp()

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

    last_qa_save_timestamp.value = datetime.datetime.now().timestamp()
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


COOKIE_MAX_AGE = 365 * 24 * 3600
MAX_KEYS_PER_BATCH = 500


def attendance_message(
        icon: str, title: str, message: str, status: int,
        detail: str = "") -> Tuple[str, int]:
    return flask.render_template(
        "attendance_message.html",
        icon=icon, title=title, message=message, detail=detail), status


def next_class_hint(now: datetime.datetime) -> str:
    """Human-readable description of the next class in the schedule."""
    upcoming = [slot for slot in schedule.slots if slot.start > now]
    if not upcoming:
        return ""
    slot = min(upcoming, key=lambda s: s.start)
    return f"The next class is {slot.course_code} on {slot.start:%Y-%m-%d %H:%M}."


@app.route("/attend/<key>")
def attendance_form(key: str) -> Tuple[str, int]:
    key = key.strip().upper()
    now = datetime.datetime.now()

    if not key_store.is_valid(key):
        return attendance_message(
            "✗", "Unknown link",
            "This check-in link is not valid.", 404)

    if key in attendance_records:
        record = attendance_records[key]
        return attendance_message(
            "✗", "Link already used",
            "This check-in link has already been used.", 410,
            detail=(f"Used by {record.name} on "
                    f"{record.time:%Y-%m-%d %H:%M}."))

    open_slots = schedule.open_slots(now)
    if not open_slots:
        return attendance_message(
            "🕒", "No class right now",
            "There is no class open for check-in at the moment. "
            "Your link has not been used up.", 200,
            detail=next_class_hint(now))

    return flask.render_template(
        "attendance_form.html",
        key=key,
        slots=open_slots,
        name=flask.request.cookies.get("student_name", ""),
        login=flask.request.cookies.get("student_login", "")), 200


@app.route("/attend/<key>", methods=["POST"])
def attendance_checkin(key: str):
    key = key.strip().upper()
    now = datetime.datetime.now()

    if not key_store.is_valid(key):
        return attendance_message(
            "✗", "Unknown link",
            "This check-in link is not valid.", 404)

    if key in attendance_records:
        record = attendance_records[key]
        return attendance_message(
            "✗", "Link already used",
            "This check-in link has already been used.", 410,
            detail=f"Used by {record.name} on {record.time:%Y-%m-%d %H:%M}.")

    name = flask.request.form.get("name", "").strip()
    login = normalize_login(flask.request.form.get("login", ""))
    if not name or not login:
        return attendance_message(
            "✗", "Missing details",
            "Please fill in both your name and your SIS login / UKČO.", 400)

    slot = schedule.slot_by_id(flask.request.form.get("slot_id", ""))
    if slot is None or not slot.is_open_at(now):
        return attendance_message(
            "🕒", "Class not open",
            "The selected class is not open for check-in. "
            "Your link has not been used up.", 400,
            detail=next_class_hint(now))

    record = Attendance(
        key=key, name=name, login=login,
        course_code=slot.course_code, lecture_code=slot.lecture_code,
        slot_id=slot.slot_id, timestamp=now.timestamp())

    # The same lecture is taught twice (Czech and English), so a student who
    # checks in for both variants is still counted only once.
    previous = attended_lecture(
        list(attendance_records.values()), login,
        slot.course_code, slot.lecture_code)

    attendance_records[key] = record
    last_attendance_action_timestamp.value = now.timestamp()

    attended_count = len({
        other.lecture_code for other in attendance_records.values()
        if other.login == login and other.course_code == slot.course_code})

    response = flask.make_response(flask.render_template(
        "attendance_done.html",
        record=record,
        duplicate=previous is not None,
        attended_count=attended_count))
    for cookie_name, value in [
            ("student_name", name), ("student_login", login)]:
        response.set_cookie(
            cookie_name, value, max_age=COOKIE_MAX_AGE, samesite="Lax")
    return response


@app.route("/attendance")
@auth.login_required
def attendance_dashboard() -> Tuple[str, int]:
    schedule.refresh_if_changed()
    key_store.refresh_if_changed()
    records = list(attendance_records.values())
    summary = attendance_summary(records)

    course_codes = schedule.course_codes
    lecture_codes = {
        course_code: schedule.lecture_codes(course_code)
        for course_code in course_codes}
    # Lectures that students checked in for but that are no longer scheduled.
    for course_code in course_codes:
        for student in summary.get(course_code, {}).values():
            for lecture_code in student["lecture_codes"]:
                if lecture_code not in lecture_codes[course_code]:
                    lecture_codes[course_code].append(lecture_code)

    return flask.render_template(
        "attendance_dashboard.html",
        schedule=schedule,
        summary=summary,
        course_codes=course_codes,
        lecture_codes=lecture_codes,
        orphaned_courses=sorted(set(summary) - set(course_codes)),
        open_slots=schedule.open_slots(datetime.datetime.now()),
        total_key_count=len(key_store.keys),
        unused_key_count=sum(
            1 for k in key_store.keys if k not in attendance_records)), 200


@app.route("/attendance.csv")
@auth.login_required
def attendance_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "login", "name", "course_code", "lecture_code", "slot_id",
        "timestamp", "key"])
    for record in sorted(
            attendance_records.values(), key=lambda r: r.timestamp):
        writer.writerow([
            record.login, record.name, record.course_code,
            record.lecture_code, record.slot_id,
            record.time.isoformat(timespec="seconds"), record.key])
    return flask.Response(
        output.getvalue(), mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=attendance.csv"})


def key_batch_stats() -> list:
    """Per-batch counts of used and unused keys, newest batch first."""
    stats = {}
    for entry in key_store.entries:
        batch = stats.setdefault(
            entry.batch, {"batch": entry.batch, "used": 0, "unused": 0,
                          "total": 0})
        batch["total"] += 1
        if entry.key in attendance_records:
            batch["used"] += 1
        else:
            batch["unused"] += 1
    return sorted(stats.values(), key=lambda b: b["batch"], reverse=True)


@app.route("/attendance_keys")
@auth.login_required
def attendance_keys() -> Tuple[str, int]:
    key_store.refresh_if_changed()
    unused = [entry for entry in key_store.entries
              if entry.key not in attendance_records]
    return flask.render_template(
        "attendance_keys.html",
        batches=key_batch_stats(),
        total_count=len(key_store.entries),
        unused_count=len(unused),
        used_count=len(key_store.entries) - len(unused),
        revoked_count=len(key_store.revoked),
        default_batch=datetime.datetime.now().strftime("%Y-%m-%d"),
        message=flask.request.args.get("message", "")), 200


@app.route("/attendance_keys/generate", methods=["POST"])
@auth.login_required
def attendance_generate_keys():
    try:
        count = int(flask.request.form.get("count", "0"))
    except ValueError:
        count = 0
    if not 1 <= count <= MAX_KEYS_PER_BATCH:
        return flask.redirect(
            relative_root() + "attendance_keys?" + urllib.parse.urlencode({
                "message": f"Enter a number of keys between 1 and "
                           f"{MAX_KEYS_PER_BATCH}."}))

    batch = flask.request.form.get("batch", "").strip()
    if not batch:
        batch = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # The batch name goes into a tab-separated file and into a URL.
    batch = batch.replace("\t", " ")

    revoked_count = 0
    if flask.request.form.get("revoke_first"):
        revoked_count = key_store.revoke([
            entry.key for entry in key_store.entries
            if entry.key not in attendance_records])

    key_store.generate(count, batch)

    message = f"Generated {count} keys in batch '{batch}'."
    if revoked_count:
        message = f"Invalidated {revoked_count} unused keys. " + message
    return flask.redirect(
        relative_root() + "attendance_keys/print?" + urllib.parse.urlencode(
            {"batch": batch, "message": message}))


@app.route("/attendance_keys/revoke", methods=["POST"])
@auth.login_required
def attendance_revoke_keys():
    scope = flask.request.form.get("scope", "")
    key_store.refresh_if_changed()

    if scope == "batch":
        batch = flask.request.form.get("batch", "")
        keys = [entry.key for entry in key_store.entries
                if entry.batch == batch and entry.key not in attendance_records]
        description = f"unused keys of batch '{batch}'"
    elif scope == "all":
        keys = [entry.key for entry in key_store.entries
                if entry.key not in attendance_records]
        description = "unused keys"
    elif scope == "keys":
        listed = flask.request.form.get("keys", "").replace(",", " ").split()
        # An already used key is spent anyway; revoking it would only remove
        # it from the statistics of its batch.
        keys = [key.strip().upper() for key in listed
                if key.strip().upper() not in attendance_records]
        description = "listed keys"
    else:
        return flask.redirect(
            relative_root() + "attendance_keys?" + urllib.parse.urlencode(
                {"message": "Nothing to invalidate."}))

    revoked_count = key_store.revoke(keys)
    return flask.redirect(
        relative_root() + "attendance_keys?" + urllib.parse.urlencode(
            {"message": f"Invalidated {revoked_count} {description}."}))


@app.route("/attendance_keys/print")
@auth.login_required
def attendance_print_keys() -> Tuple[str, int]:
    key_store.refresh_if_changed()
    batch = flask.request.args.get("batch")
    entries = [entry for entry in key_store.entries
               if entry.key not in attendance_records
               and (batch is None or entry.batch == batch)]
    return flask.render_template(
        "attendance_print_keys.html",
        entries=entries, batch=batch,
        message=flask.request.args.get("message", "")), 200


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
    parser.add_argument(
        "--schedule-file", default="schedule.csv",
        help="CSV file with the class schedule")
    parser.add_argument(
        "--attendance-keys-file", default="attendance_keys.txt",
        help="File with the one-time attendance keys")
    parser.add_argument(
        "--attendance-file", default="attendance.json",
        help="File to store the recorded attendance in")
    args = parser.parse_args()

    CORRECT_PASSWORD = args.password
    QUIZ_DIR = args.quiz_dir
    ANSWER_COUNTS_FILE = args.answer_counts_file
    ATTENDANCE_FILE = args.attendance_file
    SCHEDULE_FILE = args.schedule_file
    ATTENDANCE_KEYS_FILE = args.attendance_keys_file
    schedule = Schedule(SCHEDULE_FILE)
    key_store = KeyStore(ATTENDANCE_KEYS_FILE)

    load_app_state()
    load_quizes()

    app.run(host=args.host, port=args.port, debug=False)
