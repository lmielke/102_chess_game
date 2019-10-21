from rest_framework import serializers
from .models import Chess

"""rest API Serializer uses ajax call on the client site

[django standard class]
"""
class ChessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chess
        fields = ('pk', 'gameStatus', 'gameName', 'userName', 
                    'activePlayer', 'gameStatus', 'removeds', 'rochPara',
                    'moves', 'boardText', 'crateDate', 'changeDate',)