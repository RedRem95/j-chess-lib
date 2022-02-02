from typing import List, Tuple, Dict, Optional, Callable, Set


def _add(t1: Tuple[int, int], t2: Tuple[int, int]) -> Tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def _mul(t1: Tuple[int, int], mul: int) -> Tuple[int, int]:
    return t1[0] * mul, t1[1] * mul


def get_possible_moves(
    board_state: Dict[Tuple[str, int], Optional[str]], white: bool
) -> List[Tuple[Tuple[str, int], Tuple[str, int]]]:
    ret: Set[Tuple[Tuple[str, int], Tuple[str, int]]] = set()

    fun: Callable[[str], bool] = str.isupper if white else str.islower
    for origin_position, figure in board_state.items():
        if not fun(figure):
            continue
        moves = get_next_position(origin_position=origin_position, board_state=board_state)
        ret.update([(origin_position, x[0]) for x in moves])
        # print(origin_position, figure)
        # print(moves)

    return list(ret)


def kill_king_move(board_state: Dict[Tuple[str, int], Optional[str]],
                   move: Tuple[Tuple[str, int], Tuple[str, int]]) -> bool:
    f, t = move
    if (f not in board_state) or (t not in board_state):
        return False
    white = board_state[f].isupper()
    enemy: Callable[[str], bool] = str.islower if white else str.isupper
    return enemy(board_state[t]) and board_state[t] in ("k", "K")


def in_chess(board_state: Dict[Tuple[str, int], Optional[str]], white: bool) -> bool:
    opponent_moves = get_possible_moves(board_state=board_state, white=not white)
    return any(kill_king_move(board_state=board_state, move=x) for x in opponent_moves)


def is_promotion(board_state: Dict[Tuple[str, int], Optional[str]],
                 move: Tuple[Tuple[str, int], Tuple[str, int]]) -> bool:
    f, t = move
    white = board_state[f].isupper()
    target_row = 8 if white else 1
    return board_state[f] in ("p", "P") and t[1] == target_row


def get_next_position(
    origin_position: Tuple[str, int], board_state: Dict[Tuple[str, int], Optional[str]]
) -> List[Tuple[Tuple[str, int], bool]]:
    if board_state[origin_position] in _FUNCTIONS:
        return _FUNCTIONS[board_state[origin_position]](origin_position, board_state)
    return []


def _get_next_position_straight(
    origin_position: Tuple[str, int], board_state: Dict[Tuple[str, int], Optional[str]], white: bool,
    directions: List[Tuple[int, int]], max_steps: int = 8
) -> List[Tuple[Tuple[str, int], bool]]:
    j = 1
    moves = []
    hits = []
    start_pos = (ord(origin_position[0]), origin_position[1])
    enemy: Callable[[str], bool] = str.islower if white else str.isupper
    a, h = ord("a"), ord("h")
    while j <= max_steps and len(directions) > 0:
        for i, direction in reversed(list(enumerate(directions))):
            direction: Tuple[int, int]
            new_pos_tmp = _add(start_pos, _mul(direction, j))
            if not 1 <= new_pos_tmp[1] <= 8 or not a <= new_pos_tmp[0] <= h:
                del directions[i]
                continue
            new_pos: Tuple[str, int] = (chr(new_pos_tmp[0]), new_pos_tmp[1])
            if new_pos in board_state:
                if enemy(board_state[new_pos]):
                    hits.append(new_pos)
                del directions[i]
                continue
            moves.append(new_pos)
        j += 1
    return [(x, False) for x in moves] + [(x, True) for x in hits]


def _get_next_position_rook(
    origin_position: Tuple[str, int], board_state: Dict[Tuple[str, int], Optional[str]], white: bool
) -> List[Tuple[Tuple[str, int], bool]]:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return _get_next_position_straight(origin_position=origin_position, board_state=board_state, white=white,
                                       directions=directions)


def _get_next_position_knight(
    origin_position: Tuple[str, int], board_state: Dict[Tuple[str, int], Optional[str]], white: bool
) -> List[Tuple[Tuple[str, int], bool]]:
    hops = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    enemy: Callable[[str], bool] = str.islower if white else str.isupper
    start_pos = (ord(origin_position[0]), origin_position[1])
    a, h = ord("a"), ord("h")
    moves = [(chr(y[0]), y[1]) for y in (_add(x, start_pos) for x in hops) if a <= y[0] <= h and 1 <= y[1] <= 8]
    return [(x, x in board_state) for x in moves if x not in board_state or enemy(board_state[x])]


def _get_next_position_bishop(
    origin_position: Tuple[str, int], board_state: Dict[Tuple[str, int], Optional[str]], white: bool
) -> List[Tuple[Tuple[str, int], bool]]:
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    return _get_next_position_straight(origin_position=origin_position, board_state=board_state, white=white,
                                       directions=directions)


def _get_next_position_queen(
    origin_position: Tuple[str, int], board_state: Dict[Tuple[str, int], Optional[str]], white: bool
) -> List[Tuple[Tuple[str, int], bool]]:
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    return _get_next_position_straight(origin_position=origin_position, board_state=board_state, white=white,
                                       directions=directions)


def _get_next_position_king(
    origin_position: Tuple[str, int], board_state: Dict[Tuple[str, int], Optional[str]], white: bool
) -> List[Tuple[Tuple[str, int], bool]]:
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    return _get_next_position_straight(origin_position=origin_position, board_state=board_state, white=white,
                                       directions=directions, max_steps=1)


def _get_next_position_pawn(
    origin_position: Tuple[str, int], board_state: Dict[Tuple[str, int], Optional[str]], white: bool
) -> List[Tuple[Tuple[str, int], bool]]:
    direction = -1 + 2 * white
    home_row = 2 if white else 7
    moves = [(origin_position[0], origin_position[1] + direction)]
    if not 1 <= moves[0][1] <= 8:
        return []
    if origin_position[1] == home_row and moves[0] not in board_state:
        moves.append((origin_position[0], origin_position[1] + direction * 2))
    col = ord(origin_position[0])
    hits = [(chr(col + x), origin_position[1] + direction) for x in (-1, 1) if ord("a") <= col + x <= ord("h")]
    fun: Callable[[str], bool] = str.islower if white else str.isupper
    return [(x, False) for x in moves if x not in board_state] + \
           [(x, True) for x in hits if x in board_state and fun(board_state[x])]


_FUNCTIONS: Dict["str",
                 Callable[[Tuple[str, int], Dict[Tuple[str, int], Optional[str]]],
                          List[Tuple[Tuple[str, int], bool]]]] = {
    "p": lambda o, b: _get_next_position_pawn(origin_position=o, board_state=b, white=False),
    "P": lambda o, b: _get_next_position_pawn(origin_position=o, board_state=b, white=True),
    "r": lambda o, b: _get_next_position_rook(origin_position=o, board_state=b, white=False),
    "R": lambda o, b: _get_next_position_rook(origin_position=o, board_state=b, white=True),
    "n": lambda o, b: _get_next_position_knight(origin_position=o, board_state=b, white=False),
    "N": lambda o, b: _get_next_position_knight(origin_position=o, board_state=b, white=True),
    "b": lambda o, b: _get_next_position_bishop(origin_position=o, board_state=b, white=False),
    "B": lambda o, b: _get_next_position_bishop(origin_position=o, board_state=b, white=True),
    "q": lambda o, b: _get_next_position_queen(origin_position=o, board_state=b, white=False),
    "Q": lambda o, b: _get_next_position_queen(origin_position=o, board_state=b, white=True),
    "k": lambda o, b: _get_next_position_king(origin_position=o, board_state=b, white=False),
    "K": lambda o, b: _get_next_position_king(origin_position=o, board_state=b, white=True),
}
