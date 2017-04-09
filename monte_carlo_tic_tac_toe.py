"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
# import poc_ttt_gui
import poc_ttt_provided as provided
# import poc_simpletest

# poc_ttt_provided TTTBoard Class

# constants:
# EMPTY   (1)
# PLAYERX (2)
# PLAYERO (3)
# DRAW    (4)

# methods:
# switch_player(player)     returns PLAYERO in input PLAYERX and PLAYERX
# on input PLAYERO

# get_dim(self)                 returns the dimension of the board

# square(self, row, col)                    returns one of the three
# constants EMPTY, PLAYERX or PLAYERO that corresponds to contents of the
# board at position

# get_empty_squares(self)       returns list of(row,col) tuples for all
# empty squares

# move(self, row, col, player)  place player on board at position (row,col) player should be either constant PLAYERX or PLAYERO.  Does
# nothing if board square is not empty.

# clone(self)                   returns a copy of the board

# Constants for Monte Carlo simulator
# You may change the values but not their names.
NTRIALS = 15         # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
STATES = {1: "provided.EMPTY",
          2: "provided.PLAYERX",
          3: "provided.PLAYERO",
          4: "provided.DRAW",
          None: "none"}


def mc_trial(board, player):
    """ plays a game, alternating between players """
    # plays a game starting with the given player by making random moves alternating between players;
    # takes a current board and the next player to move
    # should return when the game is over
    # modified board will contain state of the game
    # doesn't return anything because it updates the board directly

    game_state = board.check_win()
    print "game_state:", STATES[game_state]
    print "player going first:", STATES[player]

    # keep playing until the game is over
    while game_state not in [provided.PLAYERX, provided.PLAYERO, provided.DRAW]:
        # retrieve a list of all possible moves (open squares)
        available_moves = board.get_empty_squares()

        # randomly pick an open square to place a move, checking that there are
        # available moves left
        try:
            random_index = random.randrange(0, len(available_moves))

        except ValueError:  # exit the while loop if there are no moves left
            print "No values left in available_moves"
            return

        random_square = available_moves[random_index]
        row = random_square[0]
        col = random_square[1]

        # move to randomly-picked open square
        board.move(row, col, player)
        # switch players
        player = provided.switch_player(player)
        # update the game state
        game_state = board.check_win()
    # print "\nFinal board state:\n", board
    # print "mc_trial(): winner:", STATES[game_state]


def traverse_grid(board, num_steps):
    """ helper method which allows traversal of the game board.
        This method returns the values of the game board in a list. """
    _values_list = [[0 for dummy_col in range(
        num_steps)] for dummy_row in range(num_steps)]

    for row in range(num_steps):
        for col in range(num_steps):
            _values_list[row][col] = board.square(row, col)
    return _values_list


def mc_update_scores(scores, board, player):
    """ scores completed game board, updating scores grid """
    # takes a grid of scores (a list of lists) with same dimensions as TTT board, a board form a completed game and which player the machine player is; scores the completed board and updates the scores grid;
    # does not return anything
    computer = player
    opponent = provided.switch_player(player)
    dim = board.get_dim()

    # find out who won
    winner = board.check_win()
    squares = traverse_grid(board, dim)
    # print "mc_update_scores(): squares:", squares

    # if game was a tie, no need to adjust scores
    if winner == provided.DRAW:
        return

    # score appropriately according to winner
    for row in range(dim):
        for col in range(dim):
            if winner == computer:
                if squares[row][col] == computer:
                    scores[row][col] += SCORE_CURRENT
                elif squares[row][col] == opponent:
                    scores[row][col] -= SCORE_OTHER
            elif winner == opponent:
                if squares[row][col] == opponent:
                    scores[row][col] += SCORE_OTHER
                elif squares[row][col] == computer:
                    scores[row][col] -= SCORE_CURRENT
    print "mc_update_scores():  scores:", scores


def get_max_score_index(board, choices_grid):
    """ returns the maximum score from a two-dimensional list of scores """
    max_score = -99
    max_score_indices = []
    dim = board.get_dim()
    scores_list = []

    for row in range(dim):
        for col in range(dim):
            if choices_grid[row][col] >= max_score:
                max_score = choices_grid[row][col]
                if max_score > -99:
                    max_score_indices.append([row, col])
                    scores_list.append(max_score)
            if choices_grid[row][col] == max_score:
                max_score_index = (row, col)

    # print "scores_list:", scores_list
    # print "max_score:", max_score
    # print "max_score_indices", max_score_indices
    # print "max_score_index", max_score_index
    return tuple(max_score_index)


def get_best_move(board, scores):
    """ takes current board and grid of scores; finds all the empty squares with maximum score and randomly returns one of them """
    # returns a (row, column) tuple to mc_move()

    # get all of the available moves/empty squares
    # print "\n\nget_best_move(): calculating best move:\n"
    best_move = None
    available_moves = board.get_empty_squares()
    # print "available_moves:", available_moves
    if len(available_moves) == 0:
        print "Error:  No more moves available"
        return None
    elif len(available_moves) == 1:
        return tuple(available_moves[0])
    
    # print "scores:", scores
    choices = [[-99 for dummy_col in range(board.get_dim())
                ] for dummy_row in range(board.get_dim())]

    # given all the open squares' indices (tuples)
    for index in available_moves:
        choices[index[0]][index[1]] = scores[index[0]][
            index[1]]  # take the associated scores
    # print "board:\n", board
    # print "choices:", choices
    best_move = get_max_score_index(board, choices)
    # print "best_move:", best_move
    return tuple(best_move)


def mc_move(board, player, trials):
    """ uses Monte Carlo simulation to return a move for machine player """
    # gets board, machine player and number of trials to run as input
    # returns a tuple as (row, column)
    print "\n\nComputer is", STATES[player]
    dim = board.get_dim()
    scores_grid = [[0 for dummy_col in range(dim)
                    ] for dummy_row in range(dim)]
    trial_num = 1
    print "\nboard:\n", board

    # set current board to be a copy of the actual game board
    current_board = board.clone()

    # play an entire game on the board randomly choosing moves for number of
    # trials
    while trial_num < trials:
        print "\n\nRunning trial #", trial_num
        # run one simulated game trial
        mc_trial(current_board, player)
        # score the resulting board and add it to a running total across all
        # game trials
        mc_update_scores(scores_grid, current_board, player)
        # reset current_board
        current_board = board.clone()
        # increment trial_num counter before next run
        trial_num += 1

    # randomly select an empty square on the board that has the maximum score
    return get_best_move(board, scores_grid)


# # Test game with the console or the GUI.  Uncomment whichever
# # you prefer.  Both should be commented out when you submit
# # for testing to save time.

# # provided.play_game(mc_move, NTRIALS, False)
# # poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
# # test = run_test_suite()
