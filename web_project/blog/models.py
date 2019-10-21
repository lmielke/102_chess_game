from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from PIL import Image


class Theme(models.Model):
    """
        Model for themes which can be created and updated by the User
    """
    importance = models.CharField(max_length=1)
    web_mode = models.CharField(max_length=25)
    topic = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    teaser = models.CharField(max_length=200)
    theme_img = models.ImageField(default='default.jpg',
                                    upload_to='theme_pics',
                                    verbose_name='Formate: jpg, gif, bmp')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()

        img = Image.open(self.theme_img.path)
        img.thumbnail((294.0, 267.0))
        print(f'image path is: {self.theme_img.path}')
        img.save(self.theme_img.path)


class Article(models.Model):
    """
        Model for Articles which can be created and updated by the User
    """
    importance = models.CharField(max_length=1)
    web_mode = models.CharField(max_length=25)
    obj_type = models.CharField(max_length=10, default="press")
    theme = models.CharField(max_length=4)
    topic = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    teaser = models.CharField(max_length=200)
    article_img = models.ImageField(default='default.jpg',
                                    upload_to='article_pics',
                                    verbose_name='Formate: jpg, gif, bmp')
    img_capt = models.CharField(max_length=45)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()

        img = Image.open(self.article_img.path)
        img.thumbnail((592.0, 296.0))
        img.save(self.article_img.path)


class Post(models.Model):
    """
        Model for Posts on a specific Article. Uses Article ID as Priimary Key
    """
    importance = models.CharField(max_length=1)
    web_mode = models.CharField(max_length=25)
    theme = models.CharField(max_length=4)
    article_field = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


def create_author_post(sender, **kwargs):
    """
        the posts iframe besides Article requires at least one comment to exist
        therefore if an article is created, this function creates the first post
    """
    if kwargs['created']:
        author_post = Post.objects.create(article_field=kwargs['instance'],
                                            web_mode=kwargs['instance'].web_mode,
                                            theme=kwargs['instance'].theme,
                                            title='Kommentar des Autors',
                                            content='Was ist ihre Meinung? Schreiben Sie mir!',
                                            author = kwargs['instance'].author)

post_save.connect(create_author_post, sender=Article)
