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

        _letters = [chr(x) for x in range(ord("a"), ord("h") + 1, 1)]
        _numbers = [str(x) for x in range(1, 8 + 1, 1)]
        _break = False

        ret: Dict[bool, List[Tuple[str, str, Optional[str]]]] = {True: [], False: []}

        pgn = pgn.strip().splitlines()[-1]
        pgn_split = [x for x in (y.strip() for y in re.split(r"\d+\.", pgn)) if len(x) > 0]
        for el in pgn_split:
            try:
                el1, el2, *_ = el.split(" ")
            except ValueError:
                break
            el1 = re.split(r"[x-]", el1)
            el2 = re.split(r"[x-]", el2)

            promo1 = None if '=' not in el1[1] else el1[1].split("=")[-1].upper()
            promo2 = None if '=' not in el2[1] else el2[1].split("=")[-1].lower()

            white_move = (el1[0][-2:], el1[1][:2], promo1)
            black_move = (el2[0][-2:], el2[1][:2], promo2)

            if white_move[0][0] in _letters and white_move[0][1] in _numbers and white_move[1][0] in _letters and \
                white_move[1][1] in _numbers:
                ret[True].append(white_move)
            else:
                _break = True
            if black_move[0][0] in _letters and black_move[0][1] in _numbers and black_move[1][0] in _letters and \
                black_move[1][1] in _numbers:
                ret[False].append(black_move)
            else:
                _break = True

            if _break:
                break

        return ret


if __name__ == "__main__":
    pgn = "1. h2-h4 c7-c5 2. f2-f4 b7-b5 3. e2-e3 a7-a6 4. Ng1-h3 g7-g5 5. Bf1-d3 b5-b4 6. c2-c3 Qd8-a5 7. Qd1-a4 Ra8-a7 8. e3-e4 Qa5-c7 9. Qa4-c6 Qc7xf4 10. a2-a4 Bf8-g7 11. Nh3-f2 c5-c4 12. Qc6-c7 Qf4xe4+ 13. Nf2xe4 e7-e6 14. Qc7-f4 d7-d5 15. Qf4-g4 Nb8-c6 16. Qg4-f3 b4xc3 17. b2-b3 Ra7-c7 18. d2xc3 Nc6-b8 19. b3xc4 Rc7-c5 20. Qf3-e2 Rc5-b5 21. Ra1-a2 Rb5-b7 22. Ne4-d2 Rb7-a7 23. h4-h5 Bc8-d7 24. Rh1-g1 Ng8-e7 25. Qe2xe6 Bd7-b5 26. a4-a5 Ra7-b7 27. Bc1-a3 Bb5xc4 28. Nd2-f1 Rb7-c7 29. Ba3-b4 Bc4-b3 30. Bd3-e4 Nb8-c6 31. Ra2-d2 Ke8-d8 32. Be4-f3 Rc7-c8 33. Qe6-e5 Nc6xb4 34. Rd2-d4 Bg7-h6 35. Bf3xd5 Bb3-c2 36. Bd5-a8+ Ne7-d5 37. g2-g3 Bc2-a4 38. c3xb4 Rh8-e8 39. Rd4-f4 Ba4-b5 40. Rf4-f6 Bb5-c4 41. Qe5-e7+ Kd8xe7 42. Rf6-b6 Bc4-d3 43. Rb6-b8 Rc8-c3 44. Rb8-c8 Rc3-b3 45. Ke1-d1 Bd3-e4 46. Rc8-c7+ Nd5xc7 47. Rg1-h1 Rb3xb4 48. Kd1-e2 Nc7-d5 49. g3-g4 Rb4-a4 50. Nf1-g3 Ra4-a1 51. Ba8xd5 Re8-h8 52. Rh1-f1 Ra1-a2+ 53. Ke2-d1 Ra2-a3 54. Ng3xe4 Ra3-d3+ 55. Kd1-e2 Rd3-d1 56. Rf1-f4 Rd1-c1 57. Ne4-g3 Rc1-e1+ 58. Ke2-d3 Re1-e4 59. Bd5-e6 Re4-b4 60. Kd3-c2 Rb4-b2+ 61. Kc2xb2 Ke7-d8 62. Be6-f5 Bh6-f8 63. Ng3-h1 Kd8-c7 64. Nh1-f2 Bf8-a3+ 65. Kb2-b3 Ba3-d6 66. Nf2-d1 Rh8-d8 67. Kb3-a4 Kc7-c6 68. Rf4-f2 Kc6-d5 69. Rf2-d2+ Kd5-c4 70. Nb1-a3+ Bd6xa3 71. Nd1-f2 Ba3-b4 72. Bf5-d3+ Kc4-c5 73. Ka4-b3 Kc5-c6 74. Bd3-f5 Bb4-c3 75. Nf2-d1 Bc3xd2 76. Nd1-e3 Kc6-b7 77. Bf5-b1 Kb7-c8 78. Bb1-g6 f7-f5 79. Kb3-c4 Bd2-b4 80. Ne3-d5 Bb4xa5 81. Nd5-b6+ Ba5xb6 82. g4xf5 a6-a5 83. h5-h6 Bb6-c7 84. Bg6xh7 Rd8-h8 85. Kc4-b3 Rh8-e8 86. Kb3-c2 Bc7-f4 87. f5-f6 a5-a4 88. Bh7-f5+ Kc8-b8 89. Bf5-d7 Re8-e3 90. h6-h7 Kb8-b7 91. Bd7-g4 Kb7-a8 92. f6-f7 Bf4-e5 93. Bg4-h3 a4-a3 94. Bh3-c8 a3-a2 95. Kc2-d2 a2-a1=B 96. h7-h8=Q Ka8-a7 97. Qh8-h2 Re3-e4 98. Qh2-h1 Ba1-c3+ 99. Kd2-d1 Ka7-b8 100. Bc8-h3 Kb8-c7 101. Qh1-f1 Kc7-b6 102. Bh3-g4 Bc3-a1 103. Bg4-e2 Re4-b4 104. Qf1-f5 Ba1-b2 105. Qf5-h7 Rb4-a4 106. Qh7-h5 Ra4-a1+ 107. Kd1-c2 Ra1-a3 108. Be2-d1 Ra3-a4 109. Kc2-d2 Ra4-a3 110. Qh5-e2 Ra3-a2 111. Bd1-a4 Ra2-a3 112. Qe2-g4 Ra3-a2 113. Qg4-d1 Ra2-a1 114. Qd1-f1 Ra1-b1 115. Qf1-f3 Rb1-d1+ 116. Ba4xd1 Kb6-a6 117. Qf3-d3+ Ka6-b6 118. Qd3-b5+ Kb6xb5 119. Kd2-e2 Bb2-c1 120. Ke2-d3 Kb5-b6 121. Bd1-b3 Kb6-b7 122. Bb3-a4 Kb7-a7 123. Ba4-d7 Be5-c7 124. Kd3-e2 Ka7-a8 125. Bd7-e8 Bc1-b2 126. Be8-a4 Bb2-c1 127. f7-f8=Q+ Ka8-a7 128. Qf8-b8+ Ka7xb8 129. Ba4-d7 Bc7-a5 130. Ke2-d3 Ba5-b4 131. Bd7-f5 Bb4-f8 132. Kd3-d4 Kb8-a8 133. Bf5-e6 Bc1-e3+ 134. Kd4-c3 Be3-c1 135. Be6-f5 Ka8-b8 136. Kc3-c2 Kb8-b7 137. Bf5-g4 Bf8-a3 138. Bg4-h3 Ba3-e7 139. Bh3-f1 Kb7-b8 140. Bf1-e2 Kb8-b7 141. Kc2-b3 Kb7-b6 142. Be2-a6 Kb6-a5 143. Kb3-a2 Ka5-a4 144. Ba6-d3 Ka4-a5 145. Ka2-b3 Bc1-f4 146. Kb3-c3 Be7-b4+ 147. Kc3-b3 Ka5-b6 148. Bd3-a6 Bb4-a5 149. Kb3-c4 Bf4-c7 150. Ba6-b5 Bc7-b8 151. Bb5-d7 Ba5-e1 152. Bd7-e6 Kb6-a7 153. Be6-d5 Bb8-e5 154. Bd5-c6 Be5-h2 155. Bc6-e4 Be1-c3 156. Kc4-b3 Ka7-b8 157. Be4-h1 Kb8-c8 158. Kb3-a4 Bc3-e1 159. Bh1-c6 Be1-c3 160. Bc6-f3 Bc3-a5 161. Ka4-b3 Kc8-d7 162. Kb3-b2 Ba5-d2 163. Bf3-d5 Bd2-a5 164. Bd5-e6+ Kd7xe6 165. Kb2-a3 Ba5-b4+ 166. Ka3-a4 Bb4-e1 167. Ka4-a3 Be1-a5 168. Ka3-a4 Ba5-b4 169. Ka4xb4 Ke6-d7 170. Kb4-c3 Kd7-d6 171. Kc3-d2 Kd6-c6 172. Kd2-c1 Kc6-d7 173. Kc1-d1 Kd7-c8 174. Kd1-c2 Kc8-b8 175. Kc2-b1 Kb8-c7 176. Kb1-a2 Kc7-d6 177. Ka2-a1 Kd6-d7 178. Ka1-b1 Kd7-e6 179. Kb1-c1 Bh2-c7 180. Kc1-d1 Bc7-b8 181. Kd1-d2 Bb8-c7 182. Kd2-e3 Bc7-b6+ 183. Ke3-f3 Bb6-f2 184. Kf3xf2 Ke6-f5 185. Kf2-f1 Kf5-f6 186. Kf1-g1 Kf6-e6 187. Kg1-f2 Ke6-d5 188. Kf2-g2 Kd5-c4 189. Kg2-h1 Kc4-b3 190. Kh1-h2 Kb3-a2 191. Kh2-g2 Ka2-b2 192. Kg2-h2 Kb2-a1 193. Kh2-g2 g5-g4 194. Kg2-f2 Ka1-b1 195. Kf2-g3 Kb1-a1 196. Kg3xg4 1/2-1/2"
    PGNPlayer.analyze_moves(pgn=pgn)
