from typing import List, Dict, Any
from interfaces import IGameMode, IPlayer, IDifficultyStrategy, IScoringStrategy
from models import Player


class SinglePlayerMode(IGameMode):

    def __init__(self, difficulty_strategy: IDifficultyStrategy,
                 scoring_strategy: IScoringStrategy):
        self._player: IPlayer = None
        self._difficulty_strategy = difficulty_strategy
        self._scoring_strategy = scoring_strategy
        self._target_score = 10

    def initialize(self) -> None:
        self._player = Player("Player 1", 0)

    def set_player_name(self, name: str) -> None:
        if self._player:
            self._player._name = name

    def next_turn(self) -> bool:
        # Single player doesn't switch turns
        return True

    def is_game_over(self) -> bool:
        return self._player.get_score() >= self._target_score


    def get_current_player(self) -> IPlayer:
        return self._player

    def get_results(self) -> Dict[str, Any]:
        return {
            'mode': 'single_player',
            'player': self._player.get_statistics()
        }

    def process_answer(self, is_correct: bool, time_taken: int) -> int:
        self._player.record_answer(is_correct)

        difficulty = self._difficulty_strategy.get_current_difficulty()
        points = self._scoring_strategy.calculate_score(is_correct, time_taken, difficulty)
        self._player.update_score(points)

        # Adjust difficulty based on performance
        self._difficulty_strategy.adjust_difficulty(self._player.get_statistics())

        return points

    def get_difficulty_strategy(self) -> IDifficultyStrategy:
        return self._difficulty_strategy


class MultiPlayerMode(IGameMode):

    def __init__(self, num_players: int, difficulty_strategy: IDifficultyStrategy,
                 scoring_strategy: IScoringStrategy):
        self._players: List[IPlayer] = []
        self._current_player_index = 0
        self._num_players = num_players
        self._difficulty_strategy = difficulty_strategy
        self._scoring_strategy = scoring_strategy
        self._target_score = 15

    def initialize(self) -> None:
        self._players = [Player(f"Player {i + 1}", i) for i in range(self._num_players)]

    def set_player_name(self, player_id: int, name: str) -> None:
        if 0 <= player_id < len(self._players):
            self._players[player_id]._name = name

    def next_turn(self) -> bool:
        self._current_player_index = (self._current_player_index + 1) % self._num_players
        return True

    def is_game_over(self) -> bool:
        return any(player.get_score() >= self._target_score for player in self._players)

    def get_current_player(self) -> IPlayer:
        return self._players[self._current_player_index]

    def get_all_players(self) -> List[IPlayer]:
        return self._players.copy()

    def get_leaderboard(self) -> List[IPlayer]:
        return sorted(self._players, key=lambda p: p.get_score(), reverse=True)

    def get_results(self) -> Dict[str, Any]:
        return {
            'mode': 'multiplayer',
            'players': [p.get_statistics() for p in self.get_leaderboard()],
            'winner': self.get_leaderboard()[0].get_name()
        }

    def process_answer(self, is_correct: bool, time_taken: int) -> int:
        current_player = self.get_current_player()
        current_player.record_answer(is_correct)

        difficulty = self._difficulty_strategy.get_current_difficulty()
        points = self._scoring_strategy.calculate_score(is_correct, time_taken, difficulty)
        current_player.update_score(points)

        # Adjust difficulty based on current player's performance
        self._difficulty_strategy.adjust_difficulty(current_player.get_statistics())

        return points

    def get_difficulty_strategy(self) -> IDifficultyStrategy:
        return self._difficulty_strategy
