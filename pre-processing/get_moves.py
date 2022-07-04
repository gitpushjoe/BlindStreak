import berserk
import pickle
import time
import numpy as np


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


puzzles = read_from_file('puzzles_test.pickle')

API_TOKEN = read_from_file('api_token.pickle')
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)

# puzzles = puzzles.sort_values('Popularity', ascending=False)
# puzzles['White'] = None
# puzzles['WhiteELO'] = np.nan
# puzzles['WhiteTitle'] = np.nan
# puzzles['Black'] = np.nan
# puzzles['BlackELO'] = np.nan
# puzzles['BlackTitle'] = np.nan
# puzzles['TimeControl'] = np.nan
# puzzles['Date'] = np.nan

# Scrape Lichess puzzles for game moves
for i in range(15090, len(puzzles)):
    game = puzzles.loc[i, 'GameURL']
    puzzles.loc[i, 'KeyMove'] = int(game.split('#')[1])
    if i < 100000:
        if i % 1000 == 100:
            save_to_file(puzzles, 'puzzles_test.pickle')  # for debugging purposes in terminal
            print(Color.BOLD + 'Saved!' + Color.END)
        game_id = game.split("/")[0].split('#')[0]
        game_info = client.games.export(game_id)
        moves = game_info['moves']
        puzzles.loc[i, 'GameMoves'] = moves
        puzzles.loc[i, 'WhiteTitle'] = game_info['players']['white'].get('user', {}).get('title', None)
        puzzles.loc[i, 'BlackTitle'] = game_info['players']['black'].get('user', {}).get('title', None)
        puzzles.loc[i, 'White'] = game_info['players']['white'].get('user', {}).get('name', "")
        puzzles.loc[i, 'Black'] = game_info['players']['black'].get('user', {}).get('name', "")
        puzzles.loc[i, 'WhiteELO'] = int(game_info['players']['white'].get('rating', 0))
        puzzles.loc[i, 'BlackELO'] = int(game_info['players']['black'].get('rating', 0))
        puzzles.loc[i, 'TimeControl'] = game_info['speed']
        puzzles.loc[i, 'Date'] = game_info['createdAt']
        print(f'{"%.3f" % (i / 1000)}% | {game_id}: \t {moves}')
        time.sleep(0.2)  # rate-limiting prevention
    else:
        print(f'{str(i).zfill(5)}')


save_to_file(puzzles, 'puzzles3.pickle')
