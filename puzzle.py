import pandas as pd
from typing import Union as U
import chess, chess.pgn
import io
import datetime


class PuzzleGroup:
    def __init__(self, puzzle):
        self.puzzle = puzzle.drop(columns=['level_0'], errors='ignore')

    def random(self, n):
        if n == 1:
            return PuzzleGroup.Puzzle(pd.DataFrame.sample(self.puzzle, n=n).reset_index(drop=True).loc[0])
        else:
            return PuzzleGroup(pd.DataFrame.sample(self.puzzle, n=n).drop(columns=['level_0'], errors='ignore').reset_index())

    def rating(self, rat_s: int, rat_e: int = 2200, pm: int = -1, n: int = 0, reset_index: bool = False):
        if pm >= 0:
            rat_s, rat_e = rat_s - pm, rat_s + pm
        return PuzzleGroup(self.puzzle.query(f'{rat_s} <= Rating <= {rat_e}').reset_index(drop=True))

    def ply(self, ply_s: int, ply_e: int = 60, pm: int = -1):
        if pm >= 0:
            ply_s, ply_e = ply_s - pm, ply_s + pm
        return PuzzleGroup(self.puzzle.query(f'{ply_s} <= KeyMove <= {ply_e}').reset_index(drop=True))

    def color(self, color):
        c = 0 if color == 'white' else 1 if color == 'black' else color
        return PuzzleGroup(self.puzzle.query(f'KeyMove % 2 == {c}').reset_index(drop=True))

    class Puzzle:
        def __init__(self, puzzle):
            self.puzzle = puzzle
            self.rating = self['Rating']
            self.key_move = int(self['KeyMove'])
            self.time_control = self['TimeControl']
            self.date = datetime.datetime.strftime(self['Date'], '%Y-%m-%d')
            self.white = {'user': self['White'],
                          'ELO': int(self['WhiteELO']),
                          'title': self['WhiteTitle']}
            self.black = {'user': self['Black'],
                          'ELO': int(self['BlackELO']),
                          'title': self['BlackTitle']}
            self.players = self.white, self.black
            self.game_moves = self['GameMoves']
            moves, len_moves = self.game_moves.split(" "), len(self.game_moves)
            self.pgn = " ".join([f'{int(i / 2) + 1}. {moves[i]}' if i % 2 == 0 \
                                     else moves[i] for i in range(len(moves))])
            self.puzzle_moves = " ".join(self.pgn.replace('. ', '.').split(' ')[:self.key_move - 1]).replace('.', '. ')
            game = chess.pgn.read_game(io.StringIO(self.puzzle_moves))
            correct_moves = []
            for m in self['Moves'].split(" "):
                move = chess.Move.from_uci(m)
                game.end().add_main_variation(move)
                correct_moves.append(str(game.end()))
                if len(correct_moves) == 1:
                    self.puzzle_start = str(game.mainline())
            self.solution = correct_moves
            if self.key_move % 2 == 0:
                self.color = 'white'
            else:
                self.color = 'black'

        def __getitem__(self, key):
            if type(key) == int:
                return self.puzzle.loc[key]
            elif type(key) == str:
                return self.puzzle[key]

        def __repr__(self):
            return str(f'[Rating: {str(self.rating).zfill(4)} | Ply: {self.key_move}] '
                       f'{self.white["user"]} ({self.white["ELO"]}) - {self.black["user"]} ({self.black["ELO"]}) '
                       f'{self.time_control} {self.date}')

    def __len__(self):
        return len(self.puzzle)

    def __repr__(self):
        return str(self.puzzle)

    def __getitem__(self, key):
        if type(key) == int:
            if key >= 0:
                return PuzzleGroup.Puzzle(self.puzzle.loc[key])
            else:
                return PuzzleGroup.Puzzle(self.puzzle.loc[len(self) + key])
        elif type(key) == str:
            return self.puzzle[key]
        elif type(key) == slice:
            res = self.puzzle.loc[key]
            if len(res) == 1:
                return PuzzleGroup.Puzzle(self.puzzle.loc[key])
            else:
                return PuzzleGroup.Puzzle(self.puzzle.loc[key])

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]