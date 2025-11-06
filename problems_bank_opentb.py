from typing import List, Any
from problems_bank_abstract import ProblemBank
from interfaces import IQuestionProvider
import requests


class OpenTBProblemBank(ProblemBank, IQuestionProvider):
    """
    Implements both ProblemBank and IQuestionProvider
    (Interface Segregation Principle)
    """

    def __init__(self, parameters: dict):
        self.__parameters = parameters
        self.__questions: List[Any] = []

    def load_questions(self) -> None:
        response = requests.get("https://opentdb.com/api.php",
                                params=self.__parameters)
        response.raise_for_status()
        data = response.json()
        self.__questions = data["results"]

    @property
    def questions(self) -> List[Any]:
        return self.__questions.copy()

    def get_questions(self) -> List[Any]:
        """IQuestionProvider interface method"""
        return self.__questions.copy()

    def get_question(self, index: int) -> Any:
        if 0 <= index < len(self.__questions):
            return self.__questions[index]
        raise IndexError("Question index out of range.")
