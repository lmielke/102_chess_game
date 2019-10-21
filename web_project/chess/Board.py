import numpy as np
from datetime import datetime
import os, time, getpass

# Board
class Board:


    def __init__(self, boardSaves=1, boardText=None):
        self.modelLocation = os.getcwd()
        self.boardState = False
        self.boardText = boardText
        self.boardSaves = boardSaves # how many boards per output
        #self.boardDrop = 0 if self.boardSaves == 1 else 64
        self.activePlayer = 0
        self.searchLevel = 0
        self.gamesPath = os.path.join(self.modelLocation, 'games')
        self.init_board()


    def init_board(self):
        wO = {"R1-1": [5], "H1-1": [3], "B1-1": [4], "Q1-1": [8], "K1-1": [99], "B1-2": [4], "H1-2": [3], "R1-2": [5]}
        wP = {"P1-1": [1], "P1-2": [1], "P1-3": [1], "P1-4": [1], "P1-5": [1], "P1-6": [1], "P1-7": [1], "P1-8": [1]}

        bP = {"P2-1": [-1], "P2-2": [-1], "P2-3": [-1], "P2-4": [-1], "P2-5": [-1], "P2-6": [-1], "P2-7": [-1], "P2-8": [-1]}
        bO = {"R2-1": [-5], "H2-1": [-3], "B2-1": [-4], "Q2-1": [-8], "K2-1": [-99], "B2-2": [-4], "H2-2": [-3], "R2-2": [-5]}

        self.initFigures = file_params = {**wO, **wP, **bO, **bP}
        initBoardText = [
                            "R1-1", "H1-1", "B1-1", "K1-1", "Q1-1", "B1-2", "H1-2", "R1-2",
                            "P1-1", "P1-2", "P1-3", "P1-4", "P1-5", "P1-6", "P1-7", "P1-8",
                            "----", "----", "----", "----", "----", "----", "----", "----",
                            "----", "----", "----", "----", "----", "----", "----", "----",
                            "----", "----", "----", "----", "----", "----", "----", "----",
                            "----", "----", "----", "----", "----", "----", "----", "----",
                            "P2-1", "P2-2", "P2-3", "P2-4", "P2-5", "P2-6", "P2-7", "P2-8",
                            "R2-1", "H2-1", "B2-1", "K2-1", "Q2-1", "B2-2", "H2-2", "R2-2",
                            ]
        self.boardText = self.boardText if self.boardText else initBoardText
        self.boardState = np.array([self.initFigures.get(fig, [0])[0] for fig in self.boardText]).reshape(8,8)
        self.boardText = np.array(self.boardText).reshape(8,8)
        # parameters np.tile: array, each number is the number of repetitionf for that dim
        self.boardOutState = np.tile(self.boardState, [self.boardSaves, 1, 1])
        self.trainingBoard = self.boardOutState.copy()
        return self.boardOutState, self.trainingBoard


    def flip_board(self):
        self.boardState = np.flip(self.boardState)*(-1)
        self.boardText = np.flip(self.boardText)
        return self


    def save_data(self, activePlayer):
        # self.trainingBoard = np.concatenate((self.trainingBoard, self.boardState), axis=0)
        # when board is saved it should always be with player one upside
        if activePlayer == 2: self.flip_board()
        #self.boardOutState = np.append(self.boardOutState, self.boardState)[64:]
        #self.trainingBoard = np.append(self.trainingBoard, self.boardOutState)
        self.fname = f"{str(datetime.now())}_chess_w_{activePlayer}".replace(':', '-').replace(' ', '-')
        print(f"saving file whith shape: {self.trainingBoard.shape}")
        np.save(os.path.join(self.gamesPath, self.fname), self.trainingBoard)
        return True


    def __repr__(self):
        if type(self.boardState==bool):
            self.boardState = [0 for i in range(1, 65)]
            return np.array(self.boardState).reshape(8,8)
        else:
            return self.boardState

if __name__=='__main__':
    board = Board()
    board.init_board()
    print(board.boardState)
    print(board.boardText)
