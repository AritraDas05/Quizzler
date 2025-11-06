from typing import Dict, Any
from interfaces import IPlayer


class Player(IPlayer):

    def __init__(self, name: str, player_id: int):
        self._name = name
        self._player_id = player_id
        self._score = 0
        self._correct_streak = 0
        self._total_answered = 0
        self._correct_answered = 0

    def get_name(self) -> str:
        return self._name

    def get_score(self) -> int:
        return self._score

    def update_score(self, points: int) -> None:
        self._score += points

    def record_answer(self, is_correct: bool) -> None:
        self._total_answered += 1
        if is_correct:
            self._correct_answered += 1
            self._correct_streak += 1
        else:
            self._correct_streak = 0

    def get_statistics(self) -> Dict[str, Any]:
        accuracy = (self._correct_answered / self._total_answered
                    if self._total_answered > 0 else 0.0)
        return {
            'name': self._name,
            'score': self._score,
            'total_answered': self._total_answered,
            'correct_answered': self._correct_answered,
            'accuracy': accuracy,
            'correct_streak': self._correct_streak
        }

    def reset(self) -> None:
        self._score = 0
        self._correct_streak = 0
        self._total_answered = 0
        self._correct_answered = 0


class Question:

    def __init__(self, question_data: Dict[str, Any]):
        self._question = question_data.get('question', '')
        self._correct_answer = question_data.get('correct_answer', '')
        self._incorrect_answers = question_data.get('incorrect_answers', [])
        self._difficulty = question_data.get('difficulty', 'medium')
        self._category = question_data.get('category', 'General')

    def get_text(self) -> str:
        return self._question

    def get_correct_answer(self) -> str:
        return self._correct_answer

    def get_all_answers(self) -> list:
        return self._incorrect_answers + [self._correct_answer]

    def get_difficulty(self) -> str:
        return self._difficulty

    def check_answer(self, answer: str) -> bool:
        return answer == self._correct_answer
