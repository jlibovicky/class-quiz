from typing import List
from dataclasses import dataclass
import xml.etree.ElementTree as ET


class Question:
    def __init__(self, text: str, answers: List[str], correct_answer: int):
        self.text = text
        self.answers = answers
        self.correct_answer = correct_answer

    @property
    def enum_answers(self):
        return enumerate(self.answers)


@dataclass
class Quiz:
    title: str
    questions: List[Question]

    @property
    def enum_questions(self):
        return enumerate(self.questions)


def parse_quiz(file_name: str) -> Quiz:
    tree = ET.parse(file_name)
    root = tree.getroot()

    assert root.tag == "quiz"

    title = root.attrib.get("title", "Quiz")
    course = root.attrib.get("course")

    questions = []
    for question in root.findall("question"):
        question_text = question.find("text").text
        answers = []
        correct_answer = None
        for i, answer in enumerate(question.findall("answer")):
            assert answer.tag == "answer"
            answer_text = answer.text
            if answer.attrib.get("correct", "false") == "true":
                correct_answer = i
            answers.append(answer_text)
        assert correct_answer is not None
        answers = [answer.text for answer in question.findall("answer")]
        questions.append(Question(question_text, answers, correct_answer))

    return Quiz(title, questions)
