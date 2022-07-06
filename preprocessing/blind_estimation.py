# Used to fetch puzzles to run some human tests to gather how much harder puzzles are when blindfolded.

from helpers import read_from_file, save_to_file
from puzzle import PuzzleGroup

if __name__ == '__main__':
    puzzles = read_from_file('puzzles3a.pickle').drop(columns=['index'])
    p = PuzzleGroup(puzzles)

    ratings = [1200, 1400, 1600, 1900]
    plies = [6.5, 12.5, 22.5, 34.5]

    #print(sum([q.key_move > 50 for q in iter(p)]))

    for r in ratings:
        for pl in plies:
            puzzle_selection = p.rating(r, pm=100).ply(pl, pm=0.5)
            if len(puzzle_selection) >= 9:
                puzzle_selection = puzzle_selection.random(9)
                print(f'{r} : ply {pl}')
                for i, pp in enumerate(list(puzzle_selection)):
                    nl = '\n'
                    sol = pp.solution
                    print(f'(Puzzle {i+1} | {pp.rating} | {pp.key_move}):  {pp.puzzle_moves} {sol[0]} \n{nl.join(sol[1:])}\n')
        print('')