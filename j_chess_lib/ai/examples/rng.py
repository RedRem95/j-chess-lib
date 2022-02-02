import logging
import random
import time
from copy import deepcopy
from datetime import timedelta
from typing import Optional
from uuid import UUID

from j_chess_lib.ai import StoreAI
from j_chess_lib.ai.board.utilities import get_possible_moves, kill_king_move, in_chess, is_promotion
from j_chess_lib.ai.container import GameState
from j_chess_lib.communication import MoveData, MatchStatusData

logger = logging.getLogger("j_chess_lib")


class Random(StoreAI):

    def __init__(self, name: str = "RNJesus", min_turn_time: int = 0):
        super().__init__(name=name)
        self._last_game_state: Optional[GameState] = None
        self._min_turn_time = min_turn_time

    def finalize_match(self, match_id: UUID, status: MatchStatusData, statistics: str):
        ret = super().finalize_match(match_id, status, statistics)
        other = status.name_player2 if status.name_player1 == self.name else status.name_player1
        score = {
            status.name_player1: status.score_player1,
            status.name_player2: status.score_player2
        }
        match_type = self.get_match(match_id=match_id)[1].match_type_value
        own_score = score[self.name]
        other_score = score[other]
        logger.info(f"{self.name} finished a {match_type.value}-match against {other} {own_score} to {other_score} => "
                    f"{'winner' if own_score > other_score else 'loser'}")
        return ret

    def finalize_game(self, game_id: UUID, match_id: UUID, winner: Optional[str], pgn: str):
        ret = super().finalize_game(game_id, match_id, winner, pgn)
        if winner == self.name:
            logger.info(f"{self.name} won against {self.get_match(match_id=match_id)[0]}\n"
                        f"{self._last_game_state.board_state.string()}")
        return ret

    def get_move(self, game_id: UUID, match_id: UUID, game_state: GameState) -> MoveData:
        start = time.perf_counter()
        self._last_game_state = game_state
        board_state = game_state.board_state.get_board()
        im_white = game_state.board_state.white_turn()
        white_from_storage = self.get_game(game_id=game_id, match_id=match_id) == self.name
        if im_white != white_from_storage:
            logger.exception(f"This does not align for {self}")
            exit(1)

        possible_moves = get_possible_moves(board_state=board_state, white=im_white)

        king_kill_moves = [x for x in possible_moves if kill_king_move(board_state=board_state, move=x)]
        if len(king_kill_moves) > 0:
            logger.info(f"{self.name} found a way to kill the King. Nice job")
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
                for move_f, move_t in possible_moves:
                    new_board = deepcopy(board_state)
                    new_board[move_t] = board_state[move_f]
                    del new_board[move_f]
                    if in_chess(board_state=new_board, white=not im_white):
                        good_moves.append((move_f, move_t))
                if len(good_moves) > 0:
                    possible_moves = good_moves

        taken_move_f, taken_move_t = random.choice(possible_moves)

        from_value = f"{taken_move_f[0]}{taken_move_f[1]}"
        to_value = f"{taken_move_t[0]}{taken_move_t[1]}"

        promotion = None
        if is_promotion(board_state=board_state, move=(taken_move_f, taken_move_t)):
            promotion = "Q"

        move_data = MoveData(from_value=from_value, to=to_value, promotion_unit=promotion)

        end = time.perf_counter()

        logger.info(f"{self.name} found {len(possible_moves)} possible moves that would be nice. "
                    f"Calculation took {timedelta(seconds=end - start)}/{timedelta(seconds=game_state.your_time)}")
        logger.info(f"{self.name} moves a \"{board_state[taken_move_f].upper()}\" {from_value}->{to_value}")
        if end - start < self._min_turn_time:
            time.sleep(self._min_turn_time - (end - start))
        return move_data
