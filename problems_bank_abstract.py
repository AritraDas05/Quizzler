from abc import ABC, abstractmethod
from typing import Any, List


class ProblemBank(ABC):

    @abstractmethod
    def load_questions(self) -> None:
        pass

    @property
    @abstractmethod
    def questions(self) -> List[Any]:
        pass

    @abstractmethod
    def get_question(self, question_index: int):
        pass
