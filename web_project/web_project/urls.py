from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from blog.views_articles import about
from config.views import set_web_style, set_web_mode, set_web_sys

urlpatterns = [
    path('', include('blog.urls')),
    path('', include('chess.urls')),
    path('about/', about, name='blog-about'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('web_style=<slug:web_style>/', set_web_style),
    path('web_mode=<str:web_mode>/', set_web_mode),
    path('web_sys=<str:web_sys>/', set_web_sys),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
