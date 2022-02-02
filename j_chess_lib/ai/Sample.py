import logging
from queue import Queue
from typing import Optional
from uuid import UUID

from j_chess_lib.ai import StoreAI
from j_chess_lib.ai.container import GameState
from j_chess_lib.communication import MoveData, MatchStatusData, MatchFormatData

_logger = logging.getLogger("j_chess_lib")


class SampleAI(StoreAI):
    _COUNTER = 1

    def __init__(self):
        super(SampleAI, self).__init__(name=f"Sample-{self.__class__._COUNTER}")
        self.__class__._COUNTER += 1
        self._w_q = Queue()
        self._b_q = Queue()

    def new_match(self, match_id: UUID, enemy: str, match_format: MatchFormatData):
        super().new_match(match_id, enemy, match_format)
        _logger.info(f"{self} started a new match against {enemy}. Match is a {match_format.match_type_value}",
                     extra={"AI": self})

    def finalize_match(self, match_id: UUID, status: MatchStatusData, statistics: str):
        super().finalize_match(match_id, status, statistics)
        enemy, match_data = self.get_match(match_id=match_id)
        _logger.info(f"{self} finished the match against {enemy}", extra={"AI": self})
        _logger.info(f"{status.name_player1:10}: {status.score_player1}", extra={"AI": self})
        _logger.info(f"{status.name_player2:10}: {status.score_player2}", extra={"AI": self})

    def new_game(self, game_id: UUID, match_id: UUID, white_player: str):
        super().new_game(game_id, match_id, white_player)
        enemy, match_data = self.get_match(match_id=match_id)
        _logger.info(f"{self} started a new game against {enemy}. White is {white_player}", extra={"AI": self})
        self._w_q = Queue()
        self._b_q = Queue()
        self._w_q.put(MoveData(from_value="f2", to="f3"))
        self._w_q.put(MoveData(from_value="g2", to="g4"))
        self._b_q.put(MoveData(from_value="e7", to="e5"))
        self._b_q.put(MoveData(from_value="d8", to="h4"))

    def finalize_game(self, game_id: UUID, match_id: UUID, winner: Optional[str], pgn: str):
        super().finalize_game(game_id, match_id, winner, pgn)
        enemy, match_data = self.get_match(match_id=match_id)
        _logger.info(f"{self} finished the game against {enemy}. Winner is {winner}", extra={"AI": self})

    def get_move(self, game_id: UUID, match_id: UUID, game_state: GameState) -> MoveData:
        white_player = self.get_game(game_id=game_id, match_id=match_id)
        im_white = white_player == self.name
        _logger.info(f"{self} is expected to move. I am {'white' if im_white else 'black'}", extra={"AI": self})
        _logger.info(game_state.board_state.fen, extra={"AI": self})
        move_data = (self._w_q if im_white else self._b_q).get()
        return move_data
