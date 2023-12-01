
# code from reference repo: https://github.com/techwithtim/Python-Checkers-AI

from constants import SQUARE_SIZE, GREY, KING
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 3 # create outline around piece for better visuals

    def __init__(self, row, col, color): # initialize piece
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self): # calculate position of piece
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self): # make piece a king piece
        self.king = True
    
    def draw(self, win): # draw piece to screen
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(KING, (self.x - KING.get_width()//2, self.y - KING.get_height()//2))

    def move(self, row, col): # move piece to new position
        self.row = row
        self.col = col
        self.calc_pos()