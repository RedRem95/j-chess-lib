import random
import time
from copy import deepcopy
from datetime import timedelta
from typing import Optional
from uuid import UUID

from j_chess_lib.ai import VerboseAI
from j_chess_lib.ai.board.utilities import (
    get_possible_moves, kill_king_move, in_chess, is_promotion, in_chess_after_move
)
from j_chess_lib.ai.container import GameState
from j_chess_lib.communication import MoveData


class Random(VerboseAI):

    def __init__(self, name: str = "RNJesus", min_turn_time: int = 0):
        super().__init__(name=name)
        self._last_game_state: Optional[GameState] = None
        self._min_turn_time = min_turn_time

    def get_move(self, game_id: UUID, match_id: UUID, game_state: GameState) -> MoveData:
        start = time.perf_counter()
        self._last_game_state = game_state
        board_state = game_state.board_state.get_board()
        im_white = game_state.board_state.white_turn()
        white_from_storage = self.get_game(game_id=game_id, match_id=match_id) == self.name
        if im_white != white_from_storage:
            self.logger.exception(f"This does not align for {self}")
            exit(1)

        possible_moves = get_possible_moves(board_state=board_state, white=im_white)

        king_kill_moves = [x for x in possible_moves if kill_king_move(board_state=board_state, move=x)]
        if len(king_kill_moves) > 0:
            self.logger.info(f"{self.name} found a way to kill the King. Nice job")
            possible_moves = king_kill_moves
        else:
            currently_in_chess = in_chess(board_state=board_state, white=im_white)
            if currently_in_chess:
                good_moves = []
                for move_f, move_t in possible_moves:
                    new_board = deepcopy(board_state)
                    new_board[move_t] = board_state[move_f]
                    del new_board[move_f]
                    if not in_chess(board_state=new_board, white=im_white):
                        good_moves.append((move_f, move_t))
                if len(good_moves) > 0:
                    possible_moves = good_moves
            else:
                good_moves = []
                for move in possible_moves:
                    if not in_chess_after_move(board_state=board_state, move=move, white=im_white):
                        good_moves.append(move)
                if len(good_moves) > 0:
                    possible_moves = good_moves

        taken_move_f, taken_move_t = random.choice(possible_moves)

        from_value = f"{taken_move_f[0]}{taken_move_f[1]}"
        to_value = f"{taken_move_t[0]}{taken_move_t[1]}"

        promotion = None
        if is_promotion(board_state=board_state, move=(taken_move_f, taken_move_t)):
            promotion = "Q" if im_white else "q"

        move_data = MoveData(from_value=from_value, to=to_value, promotion_unit=promotion)

        end = time.perf_counter()

        self.logger.info(f"{self.name} found {len(possible_moves)} possible moves that would be nice. "
                         f"Calculation took {timedelta(seconds=end - start)}/{timedelta(seconds=game_state.your_time)}")
        self.logger.info(f"{self.name} moves a \"{board_state[taken_move_f].upper()}\" {from_value}->{to_value}"
                         f"{f' it becomes {promotion}' if promotion else ''}")
        if end - start < self._min_turn_time:
            time.sleep(self._min_turn_time - (end - start))
        return move_data
