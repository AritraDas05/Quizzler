import html
import random
from typing import List, Optional
from interfaces import IQuestionProvider
from models import Question
from problems_bank_abstract import ProblemBank


class QuestionManager:

    def __init__(self, question_provider: IQuestionProvider):
        self._provider = question_provider
        self._questions: List[Question] = []
        self._current_index = 0

    def load_questions(self) -> None:
        self._provider.load_questions()
        raw_questions = self._provider.get_questions()

        self._questions = []
        for raw_q in raw_questions:
            raw_q['question'] = html.unescape(raw_q.get('question', ''))
            raw_q['correct_answer'] = html.unescape(raw_q.get('correct_answer', ''))
            raw_q['incorrect_answers'] = [html.unescape(ans)
                                          for ans in raw_q.get('incorrect_answers', [])]
            self._questions.append(Question(raw_q))

        random.shuffle(self._questions)

    def get_current_question(self) -> Optional[Question]:
        if 0 <= self._current_index < len(self._questions):
            return self._questions[self._current_index]
        return None

    def get_shuffled_options(self) -> List[str]:
        question = self.get_current_question()
        if question:
            options = question.get_all_answers()
            random.shuffle(options)
            return options
        return []

    def next_question(self) -> bool:
        self._current_index += 1
        return self._current_index < len(self._questions)

    def has_more_questions(self) -> bool:
        return self._current_index < len(self._questions)

    def reset(self) -> None:
        self._current_index = 0
        random.shuffle(self._questions)
