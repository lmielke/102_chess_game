import multiprocessing
from Figure import Figures
from Board import Board
# from Network import Network # nncommentout
import itertools, os, copy, random
from collections import defaultdict, deque
import numpy as np
from numpy.random import choice
import random as rd
import random, time
import tensorflow as tf
import re, getpass
import datetime as dt
# import tensorflow as tf # nncommentout
print(dt.datetime.now())
print(os.getcwd())

# Player
class Player:

    def __init__(self, boardText, boardSaves, gameType):
        self.gameType = gameType
        self.boardSaves = boardSaves
        self.board = Board(boardSaves=boardSaves, boardText=boardText)
        self.figures = Figures(self.board)
        self.blackMoves, self.whiteMoves = defaultdict(list), defaultdict(list)
        self.modelPath = os.path.join(os.getcwd(), 'chess', 'model')
        self.model = None
        self.moveHistory = deque([])
        self.allMoves = dict()
        print(f"modelPath: {self.modelPath}")

    def init_game(self):
        figures.get_moves()
        return True

    def max_play(self, maxLevel=1, activePlayer=1, scoreMethod='choice', level=1, selection=None):
        moveScore = 0
        playSwitch = itertools.cycle((1, 2))
        if activePlayer == 2: activePlayer == next(playSwitch)
        try:
            for move in range(maxLevel):
                if selection:
                    if not self.figures.set_figure(selection, activePlayer, level): raise
                    activePlayer = next(playSwitch)
                    self.board.flip_board()
                allMoves = self.figures.get_moves(activePlayer)
                moves = [m for moves in allMoves.values() for m in moves]
                #self.out_moves = [(elem[1], *elem[-2:]) for elem in moves]
                # print(f"\n\nmax_play active player: {activePlayer} at level {level} of maxLevel: {maxLevel} with move: {move} **************")
                # get maximum move score and associated move
                if maxLevel > level:
                    self.testBoards = list()
                    # print(f"max_play down now flipping board to {activePlayer} with: moveScore: {moveScore}, selection: {selection}")
                    for nextMove in moves:
                        selfBoards = (copy.deepcopy(self.board.boardText), copy.deepcopy(self.board.boardState))
                        # print(f"--> max_play going level {level+1} with Player{activePlayer} move: {move} sel: {nextMove}")
                        score, _ = self.max_play(maxLevel=1, 
                                                activePlayer=activePlayer, 
                                                scoreMethod=scoreMethod, 
                                                level=level+1, 
                                                selection=nextMove
                                                )
                        if score > moveScore:
                            moveScore = score
                            selection = nextMove
                        # print(f"max_play best selection: {selection} and score {moveScore} vs. moveScore: {moveScore}")
                        self.board.boardText, self.board.boardState = selfBoards
                else:
                    moveScore = self.maximize(activePlayer, scoreMethod=scoreMethod, selection=selection)

            # if network repeats moves, then a better move is enforced
            if level == 0:
                if selection in self.moveHistory:
                    moveScore = 0
                    for nextMove in moves:
                        score = self.maximize(activePlayer, scoreMethod='choice', selection=nextMove)
                        if score > moveScore:
                            moveScore = score
                            selection = nextMove
                self.moveHistory.append(selection)
                if len(self.moveHistory) >= 15: self.moveHistory.popleft()
            return moveScore, selection
        except Exception as e:
            print(f"max play: {e}")
            return moveScore, selection

    def play(self, player, scoreMethod, activePlayer=1, rochPara=None):
        if rochPara: self.figures.rochPara = rochPara
        playerColor = activePlayer
        # load neural network for classification
        currentModel = sorted(os.listdir(self.modelPath), reverse=True)
        if len(currentModel)>1:
            self.model = tf.keras.models.load_model(os.path.join(self.modelPath, currentModel[1]))
        # initialize players
        maxLevel, level, moveScore, playSwitch = 1, 0, None, itertools.cycle((2, 1))
        # make initial move
        if self.gameType == 'play':
            selection, maxMoves = None, 1
            # try to set figure which has been returned
            boardInitial = all(np.sum(self.board.boardState[[0,1,6,7]], axis=1) == [131, 8, -8, -131])
            print(self.board.boardState)
            if playerColor == 1:
                if boardInitial:
                    self.allMoves = self.figures.get_moves(activePlayer)
                    return self.board.boardText, self.allMoves, self.figures.removed, self.figures.rochPara
                else:
                    activePlayer = next(playSwitch)
                    self.board.flip_board()
        else:
            selection = random.choice(selection1) if activePlayer == 1 else random.choice(selection2)
            maxMoves = 50
        print(f"\nInit: playerColor: {playerColor}, activePlayer: {activePlayer}, \
        gameType: {self.gameType}\n{self.board.boardText}")
        try:
            for move in range(maxMoves):
                # go to max player and get optimal move
                if not selection:
                    mainBoards = (copy.deepcopy(self.board.boardText), copy.deepcopy(self.board.boardState))
                    moveScore, selection = self.max_play(maxLevel=maxLevel, 
                                                            activePlayer=activePlayer, 
                                                            scoreMethod=scoreMethod, 
                                                            level=level, 
                                                            selection=None)
                    self.board.boardText, self.board.boardState = mainBoards
                
                # move figure and check if move was valid or game over
                validMove = self.figures.set_figure(selection, activePlayer, level)
                # when board is saved it should always be with player one upside
                if activePlayer == 1:
                    print(f"\n\nPlayer 1: M: {move}, S: {moveScore}, {selection}\n{self.board.boardText}")
                    self.board.boardOutState = np.append(self.board.boardOutState, self.board.boardState)[64:]
                    self.board.trainingBoard = np.append(self.board.trainingBoard, self.board.boardOutState)
                self.board.flip_board()
                if activePlayer == 2:
                    print(f"\n\nPlayer 2: M: {move}, S: {moveScore}, {selection}\n{self.board.boardText}")
                    self.board.boardOutState = np.append(self.board.boardOutState, self.board.boardState)[64:]
                    self.board.trainingBoard = np.append(self.board.trainingBoard, self.board.boardOutState)
                if not validMove:
                    raise
                activePlayer = next(playSwitch)
                selection = None
            if level == 0: 
                self.allMoves = self.figures.get_moves(activePlayer)
                self.removed = self.figures.removed
                if playerColor == 2: self.board.flip_board()
            return self.board.boardText, self.allMoves, self.figures.removed, self.figures.rochPara

        except Exception as e:
            if self.gameType != 'play': player.board.save_data(activePlayer)
            print(f"\nWining:{activePlayer}, {selection} after {move}, \n{self.board.boardText}")
            print(f"play: {e}")
            if playerColor == 2: self.board.flip_board()
            return self.board.boardText, self.allMoves, self.figures.removed, self.figures.rochPara


    def maximize(self, activePlayer, scoreMethod='choice', selection=None):
        try:
            if scoreMethod == "choice":
                moveScore = max((abs(selection[0]*selection[3]) - selection[2]/3), 1) + min(selection[-1][0], 3)
                moveScore = min(max(int(random.gauss(moveScore, moveScore/5)), 1), 100)
            if scoreMethod == "network":
                moveScore = self.evaluate_board(activePlayer=activePlayer)
            return moveScore
        except Exception as e:
            print(f"maximize: {e}")
            return moveScore


    def evaluate_board(self, activePlayer):
        # send scoreRequest to Network and send board
        try:
            boardOutState = copy.deepcopy(self.board.boardOutState)
            # for some reason boardOutState gets here not as flat list if "play", but had no time to debug
            boardOutState = boardOutState.flatten()[64:] if self.gameType == "play" else boardOutState[64:]
            boardState = copy.deepcopy(self.board.boardState)
            boardOutState = boardOutState if activePlayer == 1 else np.flip(boardOutState)*(-1)
            boardState = np.flip(boardState)*(-1)
            self.evalBoard = np.append(boardOutState, boardState)
            self.evalBoard = self.evalBoard.reshape(-1, 8, 8, self.boardSaves)/10
            moveScore = np.argmax(self.model.predict(self.evalBoard))
        except Exception as e:
            print(f"evaluate board: {e}")
        return moveScore

def main(player, gameType='generate', boardText=None, activePlayer=1, rochPara=None):
    board = None
    boardSaves = 2 # how many boards are appended to output array for nn training
    scoreMethod = 'network' # network or choice
    print(f'\nprocess: {os.getpid()} starting to play with player {activePlayer} using {player}')
    player.__init__(boardText=boardText, boardSaves=boardSaves, gameType=gameType)
    board, allMoves, removed, rochPara = player.play(player, 
                                                        scoreMethod=scoreMethod, 
                                                        activePlayer=activePlayer,
                                                        rochPara=rochPara)
    return board, allMoves, removed, rochPara

def multiprocess(board):
    gameType = 'generate'
    numberProcesses = 1#multiprocessing.cpu_count()
    p = multiprocessing.Pool(processes=numberProcesses)
    out = p.map(main, [Player(boardText=board, boardSaves=1, gameType='generate') for i in range(numberProcesses)])
    p.close()
    print(f"######### MAIN FINISHED #########")
    return out

selection1 = [(2, "P1-2", 1, 0, "----", (1, 1), (random.choice([2, 3]), 1)), 
                                (2, "P1-3", 1, 0, "----", (1, 2), (random.choice([2, 3]), 2)), 
                                (2, "P1-4", 1, 0, "----", (1, 3), (random.choice([2, 3]), 3)), 
                                (2, "P1-5", 1, 0, "----", (1, 4), (random.choice([2, 3]), 4)), 
                                (2, "P1-6", 1, 0, "----", (1, 5), (random.choice([2, 3]), 5))]
selection2 = [(2, "P2-2", 1, 0, "----", (1, 1), (random.choice([2, 3]), 1)), 
                                (2, "P2-3", 1, 0, "----", (1, 2), (random.choice([2, 3]), 2)), 
                                (2, "P2-4", 1, 0, "----", (1, 3), (random.choice([2, 3]), 3)), 
                                (2, "P2-5", 1, 0, "----", (1, 4), (random.choice([2, 3]), 4)), 
                                (2, "P2-6", 1, 0, "----", (1, 5), (random.choice([2, 3]), 5))]

boardText = [   "R1-1", "H1-1", "B1-1", "K1-1", "Q1-1", "B1-2", "H1-2", "R1-2",
                "P1-1", "P1-2", "P1-3", "P1-4", "P1-5", "P1-6", "P1-7", "P1-8",
                "----", "----", "----", "----", "----", "----", "----", "----",
                "----", "----", "----", "----", "----", "----", "----", "----",
                "----", "----", "----", "----", "----", "----", "----", "----",
                "----", "----", "----", "----", "----", "----", "----", "----",
                "P2-1", "P2-2", "P2-3", "P2-4", "P2-5", "P2-6", "P2-7", "P2-8",
                "R2-1", "H2-1", "B2-1", "K2-1", "Q2-1", "B2-2", "H2-2", "R2-2",
                ]

if __name__ == '__main__':
    gameType = 'generate' # play or generate
    gameNumber = 1 # if gameType = "generate" player needs to know number of games to play
    activePlayer = 1
    rochPara=None

    if gameType == 'play':
        player = Player(boardText=boardText, boardSaves=1, gameType=gameType)
        board, allMoves, removed, rochPara = main(player, 
                                    gameType=gameType, 
                                    boardText=boardText, 
                                    activePlayer=activePlayer,
                                    rochPara=rochPara)
        print(f"\nback in main with: m: {allMoves}, r: {removed}, board:\n{board}, \nrochPara: {rochPara}")
    else:
        for _ in range(gameNumber):
            time.sleep(1)
            multiprocess(None)
