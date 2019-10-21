
"""Customization of your App in admin view
    you can change Listview and Form
"""
from django.contrib import admin
from .models import Chess

admin.site.site_header = 'Chess Dashboard'



class ChessAdmin(admin.ModelAdmin):
    """change Listview here"""
    # defines the fields to be displayed in Listview
    list_display = ('gameName', 'userName',
                    'activePlayer', 'gameStatus', 'crateDate', 'changeDate',)
    # defines the Fields you can filter by in Listview
    list_filter = ('gameName',)

    """change Form fields here"""
    # in/exclude fields from admin Form
    # fields = ('city', )

admin.site.register(Chess, ChessAdmin)

