import pickle
from typing import Union
import pandas as pd

def save_to_file(datum, location):
    pickle.dump(datum, open(location, "wb"))


def read_from_file(location):
    with open(location, "rb") as f:
        return pickle.load(f)


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def get_from_range(self, ratings: tuple = (800, 1000), plys: Union[int, tuple] = (5, 5)) -> pd.Series:
        rat_s, rat_e = ratings
        ply_s, ply_e = plys
        return pd.DataFrame.query(self.puzzle, f'{rat_s} <= Rating <= {rat_e} & {ply_s} <= KeyMove <= {ply_e}')