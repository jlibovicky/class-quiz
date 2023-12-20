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
