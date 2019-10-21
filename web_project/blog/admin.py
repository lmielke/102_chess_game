from django.contrib import admin
from . models import Post, Article, Theme

admin.site.site_header = 'Admin Console'


class ArticleAdmin(admin.ModelAdmin):
    """change Listview here"""
    # defines the fields to be displayed in Listview
    list_display = ('pk', 'obj_type', 'web_mode', 'title','importance',)
    # defines the Fields you can filter by in Listview
    list_filter = ('web_mode', 'obj_type',)
admin.site.register(Article, ArticleAdmin)

admin.site.register(Post)


class ThemeAdmin(admin.ModelAdmin):
    """change Listview here"""
    # defines the fields to be displayed in Listview
    list_display = ('pk', 'web_mode', 'topic', 'title','importance',)
    # defines the Fields you can filter by in Listview
    list_filter = ('web_mode',)

admin.site.register(Theme, ThemeAdmin)