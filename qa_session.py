from typing import List
from multiprocessing import Manager

class StudentQuestion:
    def __init__(self, question_text: str, manager: Manager):
        self.text = question_text
        self.likes = manager.Value("i", 0)
        self.dislikes = manager.Value("i", 0)

    def like(self):
        self.likes.value += 1

    def dislike(self):
        self.dislikes.value += 1

    @property
    def score(self):
        return self.likes.value - self.dislikes.value

class QASession:
    def __init__(self, timestamp: str, manager: Manager):
        self.timestamp = timestamp
        self.questions: List[StudentQuestion] = manager.list()
        self.allows_votes = manager.Value("b", False)

    def add_question(self, question_text: str, manager: Manager):
        self.questions.append(StudentQuestion(question_text, manager))

    @property
    def question_count(self):
        return len(self.questions)

    @property
    def total_votes(self):
        return sum(q.likes + q.dislikes for q in self.questions)

    def sorted_questions(self):
        return sorted(self.questions, key=lambda q: q.score, reverse=True)