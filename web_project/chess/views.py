from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from .serializers import ChessSerializer
from .models import Chess
from .forms import ChessForm
from web_project.settings import CHPID
from web_project.helper import MyHelper
import numpy as np
import os
import json


class ChessMainView(LoginRequiredMixin, CreateView):
    form_class = ChessForm
    template_name = 'chess/v_chess_main.html'
    extensions = ['blog/base.html']
    path = '/media/chess_pics/'
    success_url = '/chess/'
    view_args = {'page_title': "Chess Game",
                    'template_name': template_name,
                    'extensions': extensions}


    def get_context_data(self, *args, **kwargs):
        """09-2019: gets params for game creation and displaye them to the user for selection
        
        [user needs to specify a gameName and a playerColor to create initial board]
        
        Arguments:
            *args {[type]} -- [django default]
            **kwargs {[type]} -- [django defaults]
        
        Returns:
            [dict] -- [context object for chess entry screen]
            {allGames} -- [user sees all games and can select and switch between existing games]
        """
        context = super(ChessMainView, self).get_context_data(*args, **kwargs)
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context.update(MyHelper.get_context_metadata(self, ChessMainView.view_args))
        allGames = [name.gameName for name in Chess.objects.all()]
        context.update({'extension': self.extensions[0],
                        'template_name': self.template_name,
                        'allGames': allGames,
                        'chPid': CHPID,
                        'theme' : '21',
                        'board': {'gameStatus': 'None'}})
        Chess.game_pk = None
        return context


    def form_valid(self, form):
        """  09-2019     
        [gets the default board record from db and merges it with user entry values
        from the form, then saves result as a new game record in dbhash]
        
        Arguments:
            form {[class]} -- [user entry form for gameName and playerColor]
        
        Returns:
            [record in db] -- [saved to db, contains boardText and game paarams]
        """
        board = Chess.objects.get(gameName='default_00')
        boardText = json.loads(board.boardText)
        # board is saved as user specifies (black/white) but class Player always gets a white
        print(f"saving: {board.rochPara}")
        #if form.instance.activePlayer == '2':
        boardText = list(np.flip(np.array(boardText).reshape(8,8)).reshape(64))
        form.instance.userName = self.request.user
        form.instance.gameStatus = board.gameStatus
        form.instance.removeds = board.removeds
        form.instance.rochPara = board.rochPara
        form.instance.moves = '' 
        form.instance.boardText = json.dumps(boardText)
        messages.success(self.request, 'Lets go!')
        valid_form = super().form_valid(form)
        if valid_form:
            return HttpResponseRedirect(valid_form.url+f'Game={Chess.game_pk}')

        
class ChessInitView(LoginRequiredMixin, DetailView):
    model = Chess
    extensions = ['blog/base.html']
    template_name = 'chess/v_chess_detail.html'
    path = '/media/chess_pics/'
    view_args = {'page_title': "Chess Game",
                    'template_name': template_name,
                    'extensions': extensions}

    def get(self, request, pk):
        """09-2019 sets start board for the game
        
        - the init board is either a black or white board and is flipped accordingly
        - a html table overleys the board img and allows drag and drop of figures
        therefore each td in table must have a unique id which is generated in for loop below

        
        Arguments:
            request {django object} -- all user request information
            pk {int} -- index of the board you play
        
        Returns:
            dict -- context object with board and board params (game is ready for first move)
        """
        board = Chess.objects.get(pk=pk)
        boardText = json.loads(board.boardText)
        removeds = json.loads(board.removeds)
        rochPara = json.loads(board.rochPara)
        print(f"loading: {rochPara}")
        activePlayer = int(board.activePlayer)
        # create table td index needed to position and move the figures on board
        outBoard = list()
        for l, line in enumerate(np.array(boardText).reshape(8,8)):
            for c, cell in enumerate(line):
                td_id = f"{7-l}{7-c}" if activePlayer==1 else f"{l}{c}"
                img_id = f"{cell}"
                paths = self.path+str(cell) + '.png' if cell != '----' else self.path + 'empty.png'
                outBoard.append({'td_id' :td_id, 'img_id': img_id, 'paths': paths})
        removeds = {color: [self.path+f+'.png' for f in figures] for color, figures in removeds.items()}
        boardText = np.array(outBoard).reshape(8,8)
        context = {'board': board, 
                    'activePlayer': activePlayer,
                    'playerColor': 'white' if activePlayer == 1 else 'black',       
                    'removeds': removeds,
                    'rochPara': rochPara,
                    'boardText': boardText,
                    'chPid': CHPID,
                    'reload_url': '/chess/Game='+str(pk),
                    'theme' : '21',
                    'extension': self.extensions[0],}
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context.update(MyHelper.get_context_metadata(self, ChessInitView.view_args))
        return render(request, self.template_name, context)


class ChessUpdateView(viewsets.ModelViewSet):
    """ 2019-09-19
        reads current game form model, makes the next move (Player) and sends it via rest api to client
        IN: game from Cess Model Class
        OUT: rest json to be send to client
    """
    # sends the result to client
    queryset = Chess.objects.all()
    serializer_class = ChessSerializer


class ChessExitView(DetailView):
    model = Chess
    extensions = ['blog/base.html']
    template_name = 'chess/v_chess_detail.html'
    path = '/media/chess_pics/'

    def get(self, request, chPid):
        import subprocess
        from exit import exitGame
        if "localhost" in request.META['HTTP_HOST']:
            if chPid == os.getpid():
                subprocess.call(['deactivate'], shell=True)
                subprocess.call(['Taskkill', '/PID', str(chPid), '/F'], shell=True)
                # subprocess.call(['Taskkill', '/IM', 'python.exe', '/F'], shell=True)
            else:
                print(f"Procsss: {os.getpid()} not closed, because got {chPid}")
        return HttpResponseRedirect("https://en.wikipedia.org/wiki/Grandmaster_(chess)")