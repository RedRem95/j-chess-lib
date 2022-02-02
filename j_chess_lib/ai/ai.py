from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict, Any, List
from uuid import UUID

from .container import GameState
from ..communication.schema import MatchStatusData, MatchFormatData, MoveData


class AI(ABC):

    def __init__(self, name: str = None):
        self._name = f"{self.__class__.__name__}-PyAI" if name is None else name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return self.name

    @abstractmethod
    def new_match(self, match_id: UUID, enemy: str, match_format: MatchFormatData):
        pass

    @abstractmethod
    def finalize_match(self, match_id: UUID, status: MatchStatusData, statistics: str):
        pass

    @abstractmethod
    def new_game(self, game_id: UUID, match_id: UUID, white_player: str):
        pass

    @abstractmethod
    def finalize_game(self, game_id: UUID, match_id: UUID, winner: Optional[str], pgn: str):
        pass

    @abstractmethod
    def get_move(self, game_id: UUID, match_id: UUID, game_state: GameState) -> MoveData:
        pass

    # noinspection PyMethodMayBeStatic
    def metrics(self) -> List[Tuple[str, Any]]:
        return [("name", self.name)]


class DumbAI(AI, ABC):

    def new_match(self, match_id: UUID, enemy: str, match_format: MatchFormatData):
        pass

    def finalize_match(self, match_id: UUID, status: MatchStatusData, statistics: str):
        pass

    def new_game(self, game_id: UUID, match_id: UUID, white_player: str):
        pass

    def finalize_game(self, game_id: UUID, match_id: UUID, winner: Optional[str], pgn: str):
        pass


class StoreAI(AI, ABC):

    def __init__(self, name: str = None):
        super().__init__(name)
        self._match_storage: Dict[UUID, Tuple[str, MatchFormatData]] = {}
        self._game_storage: Dict[Tuple[UUID, UUID], str] = {}
        self._current_match: Optional[UUID] = None
        self._current_game: Optional[Tuple[UUID, UUID]] = None

    def get_match(self, match_id: UUID) -> Optional[Tuple[str, MatchFormatData]]:
        return self._match_storage.get(match_id, None)

    def get_game(self, game_id: UUID, match_id: UUID) -> Optional[str]:
        return self._game_storage.get((match_id, game_id), None)

    def new_match(self, match_id: UUID, enemy: str, match_format: MatchFormatData):
        self._match_storage[match_id] = (enemy, match_format)
        self._current_match = match_id

    def finalize_match(self, match_id: UUID, status: MatchStatusData, statistics: str):
        pass

    def new_game(self, game_id: UUID, match_id: UUID, white_player: str):
        self._game_storage[(match_id, game_id)] = white_player
        self._current_game = (game_id, match_id)

    def finalize_game(self, game_id: UUID, match_id: UUID, winner: Optional[str], pgn: str):
        pass

    def metrics(self) -> List[Tuple[str, Any]]:
        metrics = super().metrics()
        if self._current_match is not None:
            enemy, match = self.get_match(match_id=self._current_match)
            match: MatchFormatData
            metrics.append(("In match", self._current_match))
            metrics.append(("   against", enemy))
            metrics.append(("   match type", f"{match.match_type_data}"))
        if self._current_game is not None:
            game_id, match_id = self._current_game
            enemy, match = self.get_match(match_id=match_id)
            white_player = self.get_game(game_id=game_id, match_id=match_id)
            metrics.append(("In game", game_id))
            metrics.append(("   of match", f"{match_id} -> {match.match_type_value.value}"))
            metrics.append(("   against", enemy))
            metrics.append(("   white player", f"{white_player} <- {'me' if white_player == self.name else 'enemy'}"))
        return metrics
