"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None



def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Or None if the game is finished.
    """
    merged_board = sum(board, [])

    # If all areas is unavailable returns None
    if merged_board.count(None) == 0:
        return None

    # If there are more Xs than Os on the board, it is Os turn, otherwise it is Xs turn
    if merged_board.count(X) > merged_board.count(O):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Or None if a terminal board provided.
    """
    response = []

    # Going through rows and columns
    for i in range(3):
        for j in range(3):
            # Checking if position is free
            if board[i][j] is None:
                response.append((i, j))

    return response


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Copying the board in new one
    new_board = copy.deepcopy(board)

    # Check if actions is available
    if action in actions(new_board):
        i, j = action
        # Making action on new board
        new_board[i][j] = player(new_board)
    else:
        raise Exception('Invalid action is provided.')

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one, None otherwise.
    """
    # Define all positions in which game is won
    winner_positions = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
                        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
                        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]

    merged_board = sum(board, [])

    # Finding the winner
    if merged_board.count(X) >= 3 or merged_board.count(O) >= 3:
        for sign in (X, O):
            for position in winner_positions:
                counter = 0
                for coordinates in position:
                    i, j = coordinates
                    if board[i][j] != sign:
                        break
                    else:
                        counter += 1
                if counter == 3:
                    return sign
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    Game is over when there is no places available or someone is a winner.
    """
    return winner(board) is not None or player(board) is None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Defining all possible results
    results = { None : 0, X : 1, O : -1}
    return results[winner(board)]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    return estimating(board)[1]


def estimating(board):
    """
    Returns estimated cost and action for current board.
    """
    if terminal(board):
        return utility(board), None

    if player(board) == X:
        max_value = -10
        best_move = None

        for action in actions(board):
            temp_board = copy.deepcopy(board)
            temp_board = result(temp_board, action)
            value = estimating(temp_board)[0]
            if value > max_value:
                max_value = value
                best_move = action

        return max_value, best_move

    elif player(board) == O:
        max_value = 10
        best_move = None

        for action in actions(board):
            temp_board = copy.deepcopy(board)
            temp_board = result(temp_board, action)
            value = estimating(temp_board)[0]
            if value < max_value:
                max_value = value
                best_move = action

        return max_value, best_move
