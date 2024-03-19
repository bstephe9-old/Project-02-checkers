"""
Pieces.py
The Pieces File holds the Pieces class which is responsible for managing the pieces.
"""

from constants import SQUARE_SIZE, GREY, KING
import pygame

class Piece:
    """
    The Piece class is responsible for managing the pieces, and contains functions to initialize a piece, calculate the position of a piece,
    make a piece a king piece, draw a piece, and move a piece. The class also has two constants, PADDING and OUTLINE.
    """
    PADDING = 15
    OUTLINE = 3 # create outline around piece for better visuals

    def __init__(self, row, col, color):
        """
        The init function initializes the Piece class with a row, column, and color, and calculates the position of the piece.
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col

    def calc_pos(self):
        """
        The calc_pos function calculates the position of the piece.
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """
        The make king function makes a piece a king piece.
        """
        self.king = True
    
    def draw(self, win):
        """
        The draw function draws the piece on the board.
        """
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(KING, (self.x - KING.get_width()//2, self.y - KING.get_height()//2))

    def move(self, row, col): 
        """
        The move function moves a piece to a given row and calls the calculate position function to calculate the position of the piece.
        """
        self.row = row
        self.col = col
        self.calc_pos()
