from typing import Dict, Any
from interfaces import IDifficultyStrategy, IScoringStrategy


class AdaptiveDifficultyStrategy(IDifficultyStrategy):
    """Adaptive difficulty based on player performance (Strategy Pattern)"""

    def __init__(self):
        self._current_difficulty = "easy"
        self._difficulty_levels = ["easy", "medium", "hard"]

    def adjust_difficulty(self, player_stats: Dict[str, Any]) -> str:
        accuracy = player_stats.get('accuracy', 0.0)
        streak = player_stats.get('correct_streak', 0)
        total = player_stats.get('total_answered', 0)

        current_index = self._difficulty_levels.index(self._current_difficulty)

        # Increase difficulty
        if streak >= 3 and accuracy >= 0.7 and current_index < 2:
            self._current_difficulty = self._difficulty_levels[current_index + 1]

        # Decrease difficulty
        elif total >= 5 and accuracy < 0.4 and current_index > 0:
            self._current_difficulty = self._difficulty_levels[current_index - 1]

        return self._current_difficulty

    def get_current_difficulty(self) -> str:
        return self._current_difficulty


class StaticDifficultyStrategy(IDifficultyStrategy):
    """Fixed difficulty - doesn't change (Strategy Pattern)"""

    def __init__(self, difficulty: str = "medium"):
        self._difficulty = difficulty

    def adjust_difficulty(self, player_stats: Dict[str, Any]) -> str:
        return self._difficulty

    def get_current_difficulty(self) -> str:
        return self._difficulty


class BasicScoringStrategy(IScoringStrategy):
    """Basic scoring - 1 point per correct answer"""

    def calculate_score(self, is_correct: bool, time_taken: int, difficulty: str) -> int:
        return 1 if is_correct else 0


class TimeBonusScoringStrategy(IScoringStrategy):
    """Time-based scoring with difficulty multiplier"""

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

        # Bonus for fast answers (30s max)
        if time_taken <= 10:
            return base_score * 3
        elif time_taken <= 20:
            return base_score * 2
        else:
            return base_score
