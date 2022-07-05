import berserk
import time
from helpers import read_from_file, save_to_file, Color

if __name__ == '__main__':
    puzzles = read_from_file('puzzles_test.pickle')

    API_TOKEN = read_from_file('api_token.pickle')
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)

    # Rating is of puzzle; KeyMove is the ply of the first move before the puzzle; NbPlays is the number of plays.
    # It's used as a sort of limiter for how many puzzles should be downloaded.
    puzzles = puzzles.query('1600 <= Rating <= 2200 & 25 <= KeyMove <= 60 & NbPlays >= 9000 or \
                            1200 <= Rating <= 1600 & 13 <= KeyMove <= 24 & NbPlays >= 1250 or \
                            Rating <= 1200 & KeyMove <= 12 & NbPlays >= 25')
    puzzles.reset_index(inplace=True)

    # Scrape Lichess puzzles for game moves
    for i in range(len(puzzles)):
        game = puzzles.loc[i, 'GameURL']
        plays = puzzles.loc[i, 'NbPlays']
        #puzzles.loc[i, 'KeyMove'] = int(game.split('#')[1])
        km, rating = puzzles.loc[i, 'KeyMove'], puzzles.loc[i, 'Rating']
        if i % 1000 == 100:
            save_to_file(puzzles, 'puzzles_test-a.pickle')  # for debugging / auto-save
            print(Color.BOLD + 'Saved!' + Color.END)
        game_id = game.split("/")[0].split('#')[0]
        if puzzles.loc[i, 'GameMoves'] != puzzles.loc[i, 'GameMoves']:  # returns False if puzzle[i] has been webscraped
            moves = False
            while not moves:
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
                pop = puzzles.loc[i, 'Popularity']
                print(f'{"%.3f" % (i / len(puzzles) * 100)}% | {game_id}: \t KeyMove: {str(int(km)).zfill(2)} | Rating: {rating} | NbPlays: {rating}')
                time.sleep(0.175)  # rate-limiting prevention
        else:
            print(f'{"%.3f" % (i / len(puzzles) * 100)}% | {Color.GREEN}Skipped {game_id}! \t KeyMove: {str(int(km)).zfill(2)} | Rating: {rating} | NbPlays: {rating} {Color.END}')

    save_to_file(puzzles, 'puzzles3a.pickle')
