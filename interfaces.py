from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional


class IQuestionProvider(ABC):

    @abstractmethod
    def load_questions(self) -> None:
        pass

    @abstractmethod
    def get_question(self, index: int) -> Any:
        pass

    @abstractmethod
    def get_questions(self) -> List[Any]:
        pass


class IDifficultyStrategy(ABC):

    @abstractmethod
    def adjust_difficulty(self, player_stats: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def get_current_difficulty(self) -> str:
        pass


class IScoringStrategy(ABC):

    @abstractmethod
    def calculate_score(self, is_correct: bool, time_taken: int, difficulty: str) -> int:
        pass


class IGameMode(ABC):

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def next_turn(self) -> bool:
        pass

    @abstractmethod
    def is_game_over(self) -> bool:
        pass

    @abstractmethod
    def get_current_player(self) -> 'IPlayer':
        pass

    @abstractmethod
    def get_results(self) -> Dict[str, Any]:
        pass


class IPlayer(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_score(self) -> int:
        pass

    @abstractmethod
    def update_score(self, points: int) -> None:
        pass

    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def record_answer(self, is_correct: bool) -> None:
        pass


class IView(ABC):

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def hide(self) -> None:
        pass
