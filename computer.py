"""
Computer.py
The Computer File holds the Computer class which is responsible for managing the computer player.
 algorithm for AI to play checkers. Written by https://github.com/techwithtim
Code from reference repo: https://github.com/techwithtim/Python-Checkers-AI
"""

from copy import deepcopy
import pygame
from constants import RED, WHITE

def minimax(position, depth, max_player, game): 
    """
    The minimax function is the minimax algorithm for AI to play checkers, and has parameters position, depth, max_player, and game parameters.
    The function returns the best move for the computer to make.
    """
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
        #prints computer thinking until made a move
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    """
    The simulate move function simulates a move for the AI to make and returns the board.
    """

    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board, color, game): 
    """
    The get all moves function gets all possible moves for a given color and returns the moves.
    """
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece) # uncommenting this will show all possible AI moves
            
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves

def draw_moves(game, board, piece): 
    """
    The draw moves function draws all possible moves for a given piece.
    """
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)
