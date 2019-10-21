
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from PIL import Image
import os, sys
sys.path.append(os.path.join(os.getcwd(), 'chess'))
from chess import Player
import json
import numpy as np

"""
    Simple model to allow saving data to a db. Model requires to be imported
    to other models such as admin.py and models.py i.e.
    admin.py: from .models import Chess, admin.site.register(Chess)
    settings.py: 'Chess.apps.ChessConfig', # also see apps.py
"""
class Chess(models.Model):
    """
        Definition of model fields
            Extends:
                models.Model
    """
    
    gameName = models.CharField(max_length=10, default='0')
    userName = models.ForeignKey(User, on_delete=models.CASCADE) # or models.PROTECT 
    gameImage = models.ImageField(default='chessboard_oFsGPaG.jpg', upload_to='chess_pics', verbose_name='Formate: jpg, gif, bmp')
    activePlayer = models.CharField(max_length=5, choices=(('2', 'Black'),('1', 'White'),))
    gameStatus = models.CharField(max_length=7, choices=(('active', 'active'),
                                                            ('initial', 'initial'),
                                                            ('won', 'won'),
                                                            ('lost', 'lost'),
                                                            ('gaveup', 'gamveup'),))
    removeds = models.TextField(max_length=1000)
    rochPara = models.TextField(max_length=300)
    moves = models.TextField(max_length=1000)
    boardText = models.TextField(max_length=1000)
    crateDate = models.DateTimeField(auto_now_add=True)
    changeDate = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.gameName


    def save(self, force_insert=False, force_update=False, using=None):
        """
            Post saves image after modifying it in pil
            image is saved, then reloaded and processed         
        """

        boardText = json.loads(self.boardText)
        removeds = json.loads(self.removeds)
        rochPara = json.loads(self.rochPara)
        activePlayer = int(self.activePlayer)

        # if boardText comes from client it is a dictionary elif it comes from db its text
        boardText = [elem[1] for elem in sorted(boardText.items())] if type(boardText) == dict else boardText
        # player class always expects a black board, so white must be flipped to player format
        if activePlayer == 1:
            pass
            # boardText = list(np.flip(np.array(boardText).reshape(8,8)).reshape(64))
        # this calls the min/max player to return next move and additional state params
        player = Player.Player(boardText=boardText, boardSaves=1, gameType='play')
        # rochPara index needs to be flipped for Player
        # print(f"movels: {rochPara}, activePlayer: {activePlayer}")
        if activePlayer == 1:
            rochPara = {int(player): {figure: [[7-para if type(para)!=bool else para for para in paras] \
                                        for paras in params] for figure, params in figures.items()} \
                                        for player, figures in rochPara.items()}
        else:
            rochPara = {int(player): figures for player, figures in rochPara.items()}
        # print(f"movels0.5: {rochPara}, activePlayer: {activePlayer}")
        print(boardText)
        print(type(boardText))
        boardText, allMoves, removed, rochPara = Player.main(player, 
                                                    gameType='play', 
                                                    boardText=boardText, 
                                                    activePlayer=activePlayer,
                                                    rochPara=rochPara,
                                                    )
        # convert bardText to display format
        #if activePlayer == 1: boardText = np.flip(boardText)
        print(f"in models with:\n{boardText}")
        boardText = [elem for row in boardText for elem in row]
        self.boardText = json.dumps(boardText)

        # allowedMoves are showed to user on board; must be converted to str and index reversed
        def concat(mo):
            a, b = [str(7-m) if activePlayer == 2 else str(m) for m in mo[-1]]
            return a+b
        self.moves = {fig: [concat(mo) for mo in move] for fig, move in allMoves.items()}
        # removeds figures neeed to be added to be reflected in board removeds
        # removed[1] is the 1 in figure id i.e. R[1]-1 in R1-1
        if removed:
            if removed[1] == '1': removeds['white'].append(removed)
            if removed[1] == '2': removeds['black'].append(removed)
        self.removeds = json.dumps(removeds)

        # rochPara are used by board; must be index reversed
        if activePlayer == 1:
            rochPara = {player: {figure: [[7-para if type(para)!=bool else para for para in paras] \
                                        for paras in params] for figure, params in figures.items()} \
                                        for player, figures in rochPara.items()}
        self.rochPara = json.dumps(rochPara)
        super().save()


def get_pk(sender, **kwargs):
    """
        the posts iframe besides Article requires at least one comment to exist
        therefore if an article is created, this function creates the first post
    """
    if kwargs['created']:
        Chess.game_pk = kwargs.get('instance', '0')
        if not Chess.game_pk == str():
            Chess.game_pk = Chess.game_pk.pk
    else:
        Chess.game_pk = '0'
    return Chess.game_pk

post_save.connect(get_pk, sender=Chess)