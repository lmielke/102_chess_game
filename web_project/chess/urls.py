from django.urls import path, include
from chess.views import ChessMainView, ChessInitView, ChessUpdateView, ChessExitView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('chess', ChessUpdateView)

urlpatterns = [
    path('chess/', ChessMainView.as_view(), name='chess-init'),
    path('chess/Game=<int:pk>/', ChessInitView.as_view(), name='chess-view'),
    path('reload/chess/Game=<int:pk>/', ChessInitView.as_view(), name='chess-view'),
    path('exit/chPid= <int:chPid>/', ChessExitView.as_view(), name='exit-view'),
    path('rest/', include(router.urls))
    ]
