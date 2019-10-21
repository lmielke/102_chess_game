import numpy as np
from Board import Board
from itertools import product
import time
# Figure

class Figures:

    def __init__(self, board):
        self.board = board
        self.trackKing = {'K2-1': False, 'K1-1': False}
        self.kingThreats = dict()
        self.w, self.h = self.board.boardText.shape
        self.pawnStart = tuple([(1, i) for i in range(8)])
        self.rochPara = {1: {'K': [[False], [0, 1], [0, 6]], 'R1': [[False], [0, 0], [0, 2]], 'R2': [[False], [0, 7], [0, 5]]},
                        2: {'K': [[False], [0, 6], [0, 1]], 'R1': [[False], [0, 7], [0, 5]], 'R2': [[False], [0, 0], [0, 2]]}}
        self.removed = None
        self.wRemoved, self.bRemoved = list(), list()
        self.steps = {'P': [(1, -1), (1, 0), (1, 1)],
                        'R': tuple([(i, j) for i, j in product((-1, 0, 1), repeat=2) if abs(i) != abs(j)]),
                        'H': tuple([(i, j) for i, j in product((-2, -1, 1, 2), repeat=2) if abs(i) != abs(j)]),
                        'B': tuple([(i, j) for i, j in product((-1, 1), repeat=2)]),
                        'Q': tuple([(i, j) for i, j in product((-1, 0, 1), repeat=2) if not (i==0 and j==0)]),
                        'K': tuple([(i, j) for i, j in product((-1, 0, 1), repeat=2) if not (i==0 and j==0)]),
                    }
        self.nonzeroIndexs = np.nonzero(self.board.boardText)

    def get_moves(self, activePlayer):
        allMoves = dict()
        self.activePlayer = activePlayer
        for figureIndex in zip(self.nonzeroIndexs[0], self.nonzeroIndexs[1]):
            currMoves = list()
            figureName = self.board.boardText[figureIndex]
            figureValue = self.board.boardState[figureIndex]
            if figureValue <= 0: continue
            for step in self.steps[figureName[0]]:#first letter form figureName
                stepCount = [0, 0]
                self.tgtFieldIx = (figureIndex[0]+step[0],figureIndex[1]+step[1])
                while True:
                    stepCount = [stepCount[0] + step[0], stepCount[1] + step[1]]
                    # check for board borders and do not step outside of board
                    wOut = not (0 <= self.tgtFieldIx[0] < self.w) or not (0 <= self.tgtFieldIx[1] < self.w)
                    hOut = not (0 <= self.tgtFieldIx[0] < self.h) or not (0 <= self.tgtFieldIx[1] < self.h)
                    if wOut or hOut: break

                    tgtFieldName = self.board.boardText[self.tgtFieldIx]
                    tgtFieldValue = self.board.boardState[self.tgtFieldIx]

                    # if field is occupied by myself figure
                    if self.board.boardState[self.tgtFieldIx] > 0: break

                    # handle pawn special cases
                    if figureValue == 1:# check if pawn can move
                        # pawn can move twice if in init position
                        if (abs(stepCount[0]) > 1 and figureIndex not in self.pawnStart) or abs(stepCount[0]) > 2:
                            break
                        # pawn can only move diagonal if beatable opponent in tgtField
                        if step[1] != 0 and self.board.boardState[self.tgtFieldIx] == 0:
                            break
                        if step[1] == 0 and self.board.boardState[self.tgtFieldIx] != 0:
                            break
                    try:
                        if figureValue == 99:
                            # king rochade only possible if king has not moved
                            # possible max moves are
                            if activePlayer==1:
                                if abs(stepCount[0]) > 1 or not (-2 <= stepCount[1] <= 3): break
                                if stepCount[1] > 1 and (self.rochPara[activePlayer]['K'][0][0] or self.rochPara[activePlayer]['R2'][0][0]): break
                                if stepCount[1] < -1 and (self.rochPara[activePlayer]['K'][0][0] or self.rochPara[activePlayer]['R1'][0][0]): break
                                if (stepCount[1] == 2):
                                    self.tgtFieldIx = (self.tgtFieldIx[0] + step[0], self.tgtFieldIx[1] + step[1])
                                    continue
                            else:
                                if abs(stepCount[0]) > 1 or not (-3 <= stepCount[1] <= 2): break
                                if stepCount[1] > 1 and (self.rochPara[activePlayer]['K'][0][0] or self.rochPara[activePlayer]['R1'][0][0]): break
                                if stepCount[1] < -1 and (self.rochPara[activePlayer]['K'][0][0] or self.rochPara[activePlayer]['R2'][0][0]): break
                                if (stepCount[1] == -2):
                                    self.tgtFieldIx = (self.tgtFieldIx[0] + step[0], self.tgtFieldIx[1] + step[1])
                                    continue
                    except Exception as e:
                        print(f"1 Figure.py: {e}")
                        raise
                    # if field is occupied by opponent
                    if self.board.boardState[self.tgtFieldIx] < 0:
                        move = (4, figureName, figureValue, tgtFieldValue, tgtFieldName, figureIndex, self.tgtFieldIx)
                        currMoves.append(move)
                        break
                    currMoves.append((2, figureName, figureValue, tgtFieldValue, tgtFieldName, figureIndex, self.tgtFieldIx))
                    if figureValue == 3:
                        break
                    # if figure made it till here, move one step in same direction and test again
                    self.tgtFieldIx = (self.tgtFieldIx[0] + step[0], self.tgtFieldIx[1] + step[1])
            if currMoves: allMoves[figureName] = tuple(currMoves)
        return allMoves

    def say_chess(self):
        allMoves = self.get_moves(self.activePlayer)
        kingName = "K"+str(activePlayer)+"-1"
        kingPosition = np.nonzero(np.where(self.board.boardText == kingName, True, False))
        kingPosition = (kingPosition[0][0], kingPosition[1][0])
        threats = list()
        for key, values in allMoves.items():
            for i, value in enumerate(values):
                if value[-1] == kingPosition:
                    threats.append(key)
            if threats:
                self.kingThreats[kingName] = True
            else:
                self.kingThreats[kingName] = False

    def save_king(self):
        self.newMoves = dict()
        kingName = [key for key in self.kingThreats]
        self.newMoves[kingName[0]] = allMoves.get(kingName[0], False)

        if not self.newMoves:
            raise Exception(f'player: {self.activePlayer} lost')
        else:
            self.kingThreats = dict()
            #time.sleep(2)
        return self.newMoves


    def set_figure(self, choices, activePlayer, level):
        try:
            self.activePlayer = activePlayer
            _, figureName, figureValue, tgtFieldValue, tgtFieldName, figureIndex, nextIndex = choices
            nextBoard = np.zeros([8,8])
            nextBoard[nextIndex] = figureValue
            # set from field for moved figure to zero (figure is gone)
            self.board.boardState[figureIndex] = 0
            self.board.boardText[figureIndex] = '----'
            # beat possible opponent in target field
            if tgtFieldName != '----':
                self.removed = tgtFieldName
                if self.activePlayer == 1:
                    self.bRemoved.append(tgtFieldName)
                else:
                    self.wRemoved.append(tgtFieldName)
            # move figure to target field
            self.board.boardState[nextIndex] = figureValue
            self.board.boardText[nextIndex] = choices[1]

            # if move is a rochade
            if figureName.startswith('K'):
                self.rochPara[activePlayer]['K'][0][0] = True
                if abs(figureIndex[1] - nextIndex[1]) > 1:
                    print(f"roch:{figureName} with {figureIndex}, {nextIndex}, searching: {nextIndex} in {self.rochPara[activePlayer]['K']}")
                    knightName = 'R'+str(self.rochPara[activePlayer]['K'].index(list(nextIndex))) \
                                     + '-' + str(activePlayer)
                    knightFromTo = self.rochPara[activePlayer][knightName[:2]][1:]
                    knightSelection = (2, knightName, 5, 0, '----', knightFromTo[0], knightFromTo[1])
                    self.set_figure(knightSelection, activePlayer, level)
                    if level == 0:
                        print('now setting roch', knightName, knightFromTo, knightSelection)
                        time.sleep(1)
                        self.rochPara[activePlayer]['K'][0][0] = True
                        self.rochPara[activePlayer][knightName[:2]][0][0] = True
            knightName = figureName if figureName.startswith('R') else tgtFieldName \
                                    if tgtFieldName.startswith('R') else 'None'
            if knightName.startswith('R') and level == 0:
                knightName = knightName[0]+knightName[-1]
                self.rochPara[activePlayer][knightName][0][0] = True
            if tgtFieldName.startswith('K') and level == 0:
                print(f"\nEnd of Game: Player: {activePlayer} wins by beating {tgtFieldName}")
                return False
            else:
                return True
        except Exception as e:
            print(f"2 Figure.py: {e}")
            return False

    def __repr__(self):
        return self.positions



if __name__=='__main__':
        board = Board()
        figures = Figures(board)
        possMoves = figures.get_moves(0)
        for figure, posMove in possMoves.items():
            pass
