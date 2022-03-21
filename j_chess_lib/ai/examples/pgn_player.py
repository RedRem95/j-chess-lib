import logging
import os
import re
from typing import Dict, Tuple, List, Optional
from uuid import UUID

from j_chess_lib.ai import VerboseAI
from j_chess_lib.ai.container import GameState
from j_chess_lib.communication import MoveData

logger = logging.getLogger("j_chess_lib")


class PGNPlayer(VerboseAI):

    def __init__(self, pgn: str, name: str = "Pager"):
        super().__init__(name=name)
        self._step_counter: Dict[Tuple[UUID, UUID], int] = {}
        if os.path.exists(pgn):
            with open(pgn, "r") as f_in:
                pgn = f_in.read()
        self._moves = self.analyze_moves(pgn=pgn)

    def finalize_game(self, game_id: UUID, match_id: UUID, winner: Optional[str], pgn: str):
        super().finalize_game(game_id, match_id, winner, pgn)
        exit(1)

    def new_game(self, game_id: UUID, match_id: UUID, white_player: str):
        super().new_game(game_id, match_id, white_player)
        self._step_counter[(match_id, game_id)] = 0

    def get_move(self, game_id: UUID, match_id: UUID, game_state: GameState) -> MoveData:
        current_step = self._step_counter[(match_id, game_id)]
        is_white = self.get_game(game_id=game_id, match_id=match_id) == self.name
        move = self._moves[is_white][current_step]
        ret = MoveData(from_value=move[0], to=move[1], promotion_unit=move[2])
        self.log_move(move_data=ret)
        self._step_counter[(match_id, game_id)] = current_step + 1
        return ret

    @staticmethod
    def analyze_moves(pgn: str) -> Dict[bool, List[Tuple[str, str, Optional[str]]]]:
        ret: Dict[bool, List[Tuple[str, str, Optional[str]]]] = {True: [], False: []}

        pgn = pgn.strip().splitlines()[-1]
        pgn_split = [x for x in (y.strip() for y in re.split(r"\d+\.", pgn)) if len(x) > 0]
        for el in pgn_split:
            el1, el2, *_ = el.split(" ")
            el1 = re.split(r"[x-]", el1)
            el2 = re.split(r"[x-]", el2)

            promo1 = None if '=' not in el1[1] else el1[1].split("=")[-1].lower()
            promo2 = None if '=' not in el2[1] else el2[1].split("=")[-1].lower()

            white_move = (el1[0][-2:], el1[1][:2], promo1)
            black_move = (el2[0][-2:], el2[1][:2], promo2)

            ret[True].append(white_move)
            ret[False].append(black_move)

        return ret
