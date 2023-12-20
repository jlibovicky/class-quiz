from typing import List
from dataclasses import dataclass
import datetime
import os
import re


@dataclass
class Question:
    text: str
    answers: List[str]
    correct_answer: int

    @property
    def enum_answers(self):
        return enumerate(self.answers)


@dataclass
class Quiz:
    title: str
    questions: List[Question]
    last_modified: datetime.datetime
    path: str

    @property
    def enum_questions(self):
        return enumerate(self.questions)

    def needs_update(self):
        return self.last_modified < datetime.datetime.fromtimestamp(
            os.path.getmtime(self.path))


def parse_markdown_quiz(file_name: str) -> Quiz:
    last_modified = datetime.datetime.fromtimestamp(
        os.path.getmtime(file_name))
    quiz_title = None
    questions: List[Question] = []
    current_question = None
    current_answers: List[str] = []
    current_correct_answer = None

    def add_question():
        nonlocal current_question
        nonlocal current_answers
        nonlocal current_correct_answer
        if current_question is None:
            raise ValueError("No current question, but answers found.")
        if current_correct_answer is None:
            raise ValueError("No correct answer found.")
        if not current_answers:
            raise ValueError("No answers found.")

        questions.append(Question(
            current_question, current_answers, current_correct_answer))
        current_question = None
        current_answers = []
        current_correct_answer = None

    with open(file_name, encoding="utf-8") as f_quiz:
        for line in f_quiz:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith("# "):
                quiz_title = line[2:].strip()
            elif line.startswith("## "):
                if current_question is not None:
                    add_question()
                current_question = line[3:].strip()
            elif re.match(r"^\d+\.", line):
                num_pos = re.search(r"\d+\.", line)
                assert num_pos is not None
                answer = line[num_pos.end():].strip()
                if current_question is None:
                    raise ValueError("No current question, but answers found.")
                if answer.startswith("(*) "):
                    current_correct_answer = len(current_answers)
                    answer = answer[4:].strip()
                current_answers.append(answer)

    if quiz_title is None:
        raise ValueError("No quiz title found.")

    if current_question is not None:
        add_question()

    return Quiz(quiz_title, questions, last_modified, file_name)
