from typing import List
from multiprocessing import Manager

class StudentQuestion:
    def __init__(self, question_text: str, manager: Manager) -> None:
        self.text = question_text
        self.likes = manager.Value("i", 0)
        self.dislikes = manager.Value("i", 0)

    def like(self) -> None:
        self.likes.value += 1

    def dislike(self) -> None:
        self.dislikes.value += 1

    @property
    def score(self) -> int:
        return self.likes.value - self.dislikes.value

    def to_json(self) -> dict:
        return {
            "text": self.text,
            "likes": self.likes.value,
            "dislikes": self.dislikes.value,
        }

class QASession:
    def __init__(self, timestamp: str, manager: Manager) -> None:
        self.timestamp = timestamp
        self.questions: List[StudentQuestion] = manager.list()
        self.allows_votes = manager.Value("b", False)

    def add_question(self, question_text: str, manager: Manager) -> None:
        self.questions.append(StudentQuestion(question_text, manager))

    @property
    def question_count(self) -> int:
        return len(self.questions)

    @property
    def total_votes(self) -> int:
        return sum(q.likes.value + q.dislikes.value for q in self.questions)

    def sorted_questions(self) -> list[StudentQuestion]:
        return sorted(self.questions, key=lambda q: q.score, reverse=True)

    def to_json(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "questions": [s.to_json() for s in self.sorted_questions()],
            "allows_votes": self.allows_votes.value
        }

    @staticmethod
    def from_json_dict(json_dict: dict, manager: Manager):
        session = QASession(json_dict["timestamp"], manager)
        session.allows_votes.value = json_dict["allows_votes"]
        for question in json_dict["questions"]:
            session.add_question(question["text"], manager)
            session.questions[-1].likes.value = question["likes"]
            session.questions[-1].dislikes.value = question["dislikes"]
        return session