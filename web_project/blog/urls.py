from django.urls import path, include
from . views_articles import ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, UserArticleListView, UserThemeListView
from . views_posts import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('', UserArticleListView.as_view(), name='articles-all'),
    path('themes/', UserThemeListView.as_view(), name='blog-home'),
    path('blog/', include([
        path('articles/Theme=<int:theme>/', include([
            path('Article=0/Frame=<int:frame>/view/', UserArticleListView.as_view(), name='articles-all'),
            path('Article=<int:pk>/Frame=<int:frame>/view/', ArticleDetailView.as_view(), name='articles-detail'),
            path('Article=0/Frame=<int:frame>/add/', ArticleCreateView.as_view(), name='articles-create'),
            path('User=<str:username>/Frame=<int:frame>/view/', UserArticleListView.as_view(), name='articles-user'),
            path('Article=<int:pk>/Frame=<int:frame>/change/', ArticleUpdateView.as_view(), name='articles-update'),
            path('Article=<int:pk>/Frame=<int:frame>/delete/', ArticleDeleteView.as_view(), name='articles-delete'),]))
                            ,])),

    path('blog/', include([
        path('posts/Theme=<int:theme>/', include([
            path('Article=0/Post=0/Frame=<int:frame>/view/', UserPostListView.as_view(), name='posts-all'),
            path('Article=<int:article_field_id>/Frame=<int:frame>/view/', UserPostListView.as_view(), name='posts-topic'),
            path('User=<str:username>/Frame=<int:frame>/view/', UserPostListView.as_view(), name='posts-user'),
            path('Article=<int:article_id>/Post=<int:pk>/Frame=<int:frame>/view/', PostDetailView.as_view(), name='posts-detail'),
            path('Article=<int:article_field_id>/Frame=<int:frame>/Post=0/add/', PostCreateView.as_view(), name='posts-create'),
            path('Article=<int:article_field_id>/Post=<int:pk>/Frame=<int:frame>/change/', PostUpdateView.as_view(), name='posts-update'),
            path('Article=<int:article_field_id>/Post=<int:pk>/Frame=<int:frame>/delete/', PostDeleteView.as_view(), name='posts-delete'),]))
                            ,]))
            ,]

