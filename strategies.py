from typing import Dict, Any
from interfaces import IDifficultyStrategy, IScoringStrategy


class AdaptiveDifficultyStrategy(IDifficultyStrategy):

    def __init__(self):
        self._current_difficulty = "easy"
        self._difficulty_levels = ["easy", "medium", "hard"]

    def adjust_difficulty(self, player_stats: Dict[str, Any]) -> str:
        accuracy = player_stats.get('accuracy', 0.0)
        streak = player_stats.get('correct_streak', 0)
        total = player_stats.get('total_answered', 0)

        current_index = self._difficulty_levels.index(self._current_difficulty)

        if streak >= 3 and accuracy >= 0.7 and current_index < 2:
            self._current_difficulty = self._difficulty_levels[current_index + 1]

        elif total >= 5 and accuracy < 0.4 and current_index > 0:
            self._current_difficulty = self._difficulty_levels[current_index - 1]

        return self._current_difficulty

    def get_current_difficulty(self) -> str:
        return self._current_difficulty


class StaticDifficultyStrategy(IDifficultyStrategy):

    def __init__(self, difficulty: str = "medium"):
        self._difficulty = difficulty

    def adjust_difficulty(self, player_stats: Dict[str, Any]) -> str:
        return self._difficulty

    def get_current_difficulty(self) -> str:
        return self._difficulty


class BasicScoringStrategy(IScoringStrategy):

    def calculate_score(self, is_correct: bool, time_taken: int, difficulty: str) -> int:
        return 1 if is_correct else 0


class TimeBonusScoringStrategy(IScoringStrategy):

    def __init__(self):
        self._difficulty_multiplier = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }

    def calculate_score(self, is_correct: bool, time_taken: int, difficulty: str) -> int:
        if not is_correct:
            return 0

        base_score = self._difficulty_multiplier.get(difficulty, 1)

        if time_taken <= 3:
            return base_score * 3
        elif time_taken <= 6:
            return base_score * 2
        else:
            return base_score
