#!/usr/bin/env python3

import io
import xml.etree.ElementTree as ET

from markdown import markdown


HEADER = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Quiz</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script src="/script.js"></script>

<style>
button {
    margin: 0.25em;
}
</style>

</head>
<body>
"""

FOOTER = """</body>
</html>"""


def md(text: str) -> str:
    return markdown(text).removeprefix("<p>").removesuffix("</p>")


def generate_student_html(quiz):
    output = io.StringIO()

    print(HEADER, file=output)
    print('<div class="container">', file=output)
    print(f'<h1>{quiz.title}</h1>', file=output)

    print('<div class="accordion accordion-flush" id="accordion">', file=output)
    for q_id, question in enumerate(quiz.questions):
        print('<div class="accordion-item">', file=output)
        print(f'<h2 class="accordion-header" id="heading{q_id}">', file=output)
        print(f'<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse_{q_id}" aria-expanded="true" aria-controls="collapse_{q_id}">', file=output)
        print(f'Question {q_id + 1}', file=output)
        print('</button>', file=output)
        print('</h2>', file=output)
        show = "show" if q_id == 0 else ""
        print(f'<div id="collapse_{q_id}" class="accordion-collapse collapse {show}" aria-labelledby="heading{q_id}" data-bs-parent="#accordion">', file=output)
        print('<div class="accordion-body">', file=output)

        print('<p>{}</p>'.format(md(question.text)), file=output)

        for a_id, answer in enumerate(question.answers):
            print(f'<button type="button" class="btn btn-outline-primary w-100" onclick="toggleAnswer(this, {q_id}, {a_id})">{md(answer)}</button>', file=output)

        print('</div>', file=output)
        print('</div>', file=output)
    print('</div>', file=output)
    print(FOOTER, file=output)
    html = output.getvalue()
    output.close()
    return html


def generate_teacher_html(quiz_id, quiz, answer_cache):
    output = io.StringIO()

    stats = {}
    for key, count in answer_cache.items():
        stat_quiz_id, q_id_str, a_id_str = key.split("-")
        if quiz_id != stat_quiz_id:
            continue
        q_id, a_id = int(q_id_str), int(a_id_str)
        stats.setdefault(q_id, {})
        stats[q_id][a_id] = count

    print(HEADER, file=output)
    print('<div class="container">', file=output)
    print(f'<h1>{quiz.title}</h1>', file=output)

    for q_id, question in enumerate(quiz.questions):
        print('<div class="card mb-3">', file=output)
        print('<div class="card-body">', file=output)
        print('<h5 class="card-title">{}</h5>'.format(md(question.text)), file=output)
        print('<div class="card-text">', file=output)

        print('<table class="table table-striped">', file=output)
        for a_id, answer in enumerate(question.answers):
            count = stats.get(q_id, {}).get(a_id, 0)
            if a_id == question.correct_answer:
                print('<tr class="table-success">', file=output)
                print('<td style="width: 20%">✓</td>', file=output)
            else:
                print('<tr class="table-danger">', file=output)
                print(f'<td style="width: 20%">{count}</td>', file=output)
            print(f'<td>{md(answer)}</td>', file=output)
            print('</tr>', file=output)
        print('</table>', file=output)

        print('</div>', file=output) # card-text
        print('</div>', file=output) # card-body
        print('</div>', file=output) # card

    print('</div>', file=output)
    print(FOOTER, file=output)

    html = output.getvalue()
    output.close()
    return html
