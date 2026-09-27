# class-quiz

A simple web app for multi-choice quizzes that I give in my classes.
Open-source and lightweight Kahoot alternative. Written in Python using Flask.

It has an anonymous student interface that displays the quiz in a
smartphone-friendly format and a teacher interface that shows statistics of
incorrect answers meant to be presented to the class.

## Running the server

```bash
python3 server.py --host 0.0.0.0 --port 5000 --quiz-dir quizzes --password your-password
```

The `quizzes` directory contains Markdown files with quizzes. The
student interface is then available under `<root>/quiz/<quiz_id>` where
`<quiz_id>` is the file name without the extension.

The teacher interface is protected by a password. Quiz statistics for a
particular quiz are under `<root>/answer_stats/<quiz_id>`. The root address
shows an overview of available quizzes and allows generating a QR code that
could pasted into slides.

The page `<root>/timer/<quiz_id>?minutes=<minutes>` shows a page with a QR code
leading to the student interface. After the specified time is over, it shows
the answer statistics.

Pinging `<root>/github_update` pulls the repository and reloads the quizzes.

## Attendance tracking

Students check in to a class by scanning a QR code on a small paper slip. Each
slip carries a one-time key, so it works exactly once.

### Schedule

The classes are listed in a CSV file (`schedule.csv` by default):

```
<COURSE_CODE>,<LECTURE_CODE>,<DATE>,<START_TIME>,<END_TIME>
```

Dates are `YYYY-MM-DD` (`D.M.YYYY` is accepted too) and times are `HH:MM`.
Empty lines, lines starting with `#`, and a header line are ignored. The same
lecture given twice (e.g., once in Czech and once in English) shares the
`LECTURE_CODE`; such a lecture is counted only once per student even if the
student checks in for both. The file is re-read whenever it changes on disk.

Check-in is possible from 15 minutes before the start until 15 minutes after
the end of a class (`GRACE_BEFORE` and `GRACE_AFTER` in `attendance.py`). If
several classes are open at the same time, the student picks one.

### Keys and paper slips

The page `<root>/attendance_keys` (password protected) manages the keys:

* **Generate new keys.** Choose how many and a batch name (the date by
  default). The keys are appended to `attendance_keys.txt` and the printable
  sheet of the new batch opens right away — print it and cut it into slips.
  Ticking *Invalidate all currently unused keys first* reissues everything at
  once, which is what to do if a printed sheet leaks.
* **Invalidate keys**, either the unused keys of one batch, a few keys listed
  by their code (for a slip that was lost), or all unused keys at once. Every
  invalidation asks for confirmation first.
* **Print** the unused keys of a batch, or of all batches together.

Keys that have already been used cannot be invalidated: they are spent anyway
and the attendance recorded with them is kept. Invalidated keys stay in the
key file as `# REVOKED` comment lines, both as a record and so that the same
key is never generated again.

A key that is scanned outside class hours is not used up, so leftover slips
can be handed out again. Keys can also be generated from the command line:

```bash
python3 make_attendance_keys.py 60 --batch "2026-10-01"
```

### Student interface

The QR code leads to `<root>/attend/<key>`, which asks for the student's name
and SIS login/UKČO. Both are stored in a cookie, so the fields are prefilled
the next time. The confirmation page shows how many lectures of the course the
student has attended so far.

### Teacher interface

`<root>/attendance` (password protected) shows a table per course: one row per
student, one column per lecture code, and the total number of attended
lectures. `<root>/attendance.csv` downloads all raw check-ins. Attendance is
stored in `attendance.json`.

## Defining a quiz

Quizzes are defined Markdown documents. Math can be written using LaTeX in
dollar signs using [MathJax](https://www.mathjax.org/). Each quiz must have a
title. Questions are defined as level 2 headings. Answers are listed in a
numbered list. The correct answer must have the `(*) ` prefix. There is always
exactly one correct answer.

```markdown
# Sample quiz

## 1. What is the capital of France?

1. (*) Paris
2. London
3. Berlin
4. Madrid
5. Helsinki


## 2. What is the correct equation for the __Pythagorean theorem?__

1. $\sum_i^\infty \frac{1}{\log i}$
2. $a^2 + b^2 = e^2$
3. (*) $a^2 + b^2 = c^2$
4. $a^2 + b^2 = f^2$
```
