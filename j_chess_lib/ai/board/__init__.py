from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List


@dataclass(frozen=True)
class BoardState:
    fen: str

    def get_board(self) -> Dict[Tuple[str, int], Optional[str]]:
        ret: Dict[Tuple[str, int], Optional[str]] = {}
        row = 8
        col = ord('a')
        board_state = self.fen.strip().split(" ", maxsplit=1)[0].strip()
        for s in board_state:
            try:
                i = int(s)
                col += i
            except ValueError:
                if s == "/":
                    row -= 1
                    col = ord("a")
                else:
                    ret[(chr(col), row)] = s
                    col += 1
        return ret

    def string(self) -> str:
        b = self.get_board()
        ret: List[List[str]] = [[]]
        for row in range(8, 0, -1):
            for col in range(ord("a"), ord("h") + 1, 1):
                ret[-1].append(b.get((chr(col), row), " "))
            if row > 1:
                ret.append([])
        return "\n".join("".join(y for y in x) for x in ret)

    def white_turn(self):
        return self.fen.lower().strip().split(" ")[1] == "w"

    def __str__(self):
        return self.fen


if __name__ == '__main__':
    from j_chess_lib.ai.board.utilities import get_possible_moves, kill_king_move, is_promotion, in_chess_after_move

    for fen in [
        # "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        # "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        # "rnbqkbnr/pp1ppppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2",
        # "rnbqkbnr/pp1ppppp/8/3p4/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
        # "rnbqkbnr/pp1ppppp/8/3p4/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 2",
        # "rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR w KQkq - 1 2",
        # "rnbqkbnr/1ppppppp/8/p3Q3/P7/k7/1PPPPPPP/RNBQKBNR w KQkq - 1 2",
        # "8/4P3/8/8/8/3p4/4p3/8 b KQkq - 1 2",
        "4k3/3p4/8/1B6/8/8/8/K7 b KQkq - 1 2"
    ]:
        board = BoardState(fen=fen)
        # pprint(board.get_board())
        print(f"\n{fen}:")
        print(f"  {' '.join(chr(x) for x in range(ord('a'), ord('h') + 1, 1))}")
        print(f" ┌{'─' * (8 + 7)}┐")
        for i, line in enumerate(board.string().split("\n")):
            print(f"{8 - i}│{' '.join(line)}│{8 - i}")
        print(f" └{'─' * (8 + 7)}┘")
        print(f"  {' '.join(chr(x) for x in range(ord('a'), ord('h') + 1, 1))}")
        print("")
        moves = get_possible_moves(board_state=board.get_board(), white=board.white_turn())
        print("All      ", len(moves), moves)
        print("Kill King", [x for x in moves if kill_king_move(board_state=board.get_board(), move=x)])
        print("Promotion", [x for x in moves if is_promotion(board_state=board.get_board(), move=x)])
