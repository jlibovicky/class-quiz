# class-quiz
A simple web app for multi-choice quizzes that I give in my classes. Open-source and lightweight Kahhot alternative. Written in Python using Flask.

It has an anonymous student interface that displays the quiz in a smartphone-friendly format and a teacher interface that shows statistics of incorrect answers meant to be presented to the class.

## Running the server

```bash
python3 server.py --host 0.0.0.0 --port 5000 --quiz-dir quizzes
```

The `quizzes` directory contains XLM files with particular quizzes.
The student interface is then available under `<root>/quiz/<quiz_id>` where `<quiz_id>` is the file name without the extension.
The teacher interface is under `<root>/answer_stats/sample_quiz`.

## Defining a quiz

Quizzes are defined in an XLM format. All text fields are written using Markdown.
Math can be written using LaTeX in dollar signs using [MathJax](https://www.mathjax.org/).

```xlm
<quiz title="Sample quiz forever">
  <question>
      <text>What is the capital of France?</text>
      <answer correct="true">Paris</answer>
      <answer>London</answer>
      <answer>Berlin</answer>
      <answer>Madrid</answer>
  </question>
  <question>
      <text>What is the correct equation for the __Pythagorean theorem?__</text>
      <answer>$\sum_i^\infty \frac{1}{\log i}$</answer>
      <answer>$a^2 + b^2 = e^2$</answer>
      <answer correct="true">$a^2 + b^2 = c^2$</answer>
      <answer>$a^2 + b^2 = f^2$</answer>
  </question>
</quiz>
```
