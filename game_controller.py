from typing import Optional
from interfaces import IGameMode, IDifficultyStrategy
from question_manager import QuestionManager
from models import Question


class GameController:
    """
    Main game controller - depends on abstractions, not concretions
    (Dependency Inversion Principle)
    """

    def __init__(self, game_mode: IGameMode, question_manager: QuestionManager):
        self._game_mode = game_mode  # Depends on IGameMode abstraction
        self._question_manager = question_manager
        self._time_taken = 0

    def start_game(self) -> None:
        """Initialize and start the game"""
        self._game_mode.initialize()
        self._question_manager.load_questions()

    def get_current_question(self) -> Optional[Question]:
        return self._question_manager.get_current_question()

    def get_shuffled_options(self) -> list:
        return self._question_manager.get_shuffled_options()

    def submit_answer(self, answer: str, time_taken: int) -> tuple:
        """
        Submit answer and get result
        Returns: (is_correct, points_earned)
        """
        question = self._question_manager.get_current_question()
        if not question:
            return False, 0

        is_correct = question.check_answer(answer)
        points = self._game_mode.process_answer(is_correct, time_taken)

        return is_correct, points

    def next_question(self) -> bool:
        """Move to next question/turn"""
        has_more = self._question_manager.next_question()

        if has_more and hasattr(self._game_mode, 'next_turn'):
            self._game_mode.next_turn()

        return has_more

    def is_game_over(self) -> bool:
        return (self._game_mode.is_game_over() or
                not self._question_manager.has_more_questions())

    def get_current_player(self):
        return self._game_mode.get_current_player()

    def get_game_mode(self) -> IGameMode:
        return self._game_mode

    def get_results(self) -> dict:
        return self._game_mode.get_results()

    def get_current_difficulty(self) -> str:
        strategy = self._game_mode.get_difficulty_strategy()
        return strategy.get_current_difficulty()
