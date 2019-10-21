from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Article, Theme
from .forms import ArticleCreateForm
import os
from web_project.alice import alice
from web_project.helper import MyHelper
from django.http import HttpResponseRedirect


class UserArticleListView(ListView):
    model = Article
    template_name = 'articles/v_articles.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Überblick",
                    'template_name': template_name,
                    'extensions': extensions}
    context_object_name = 'articles'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        return context

    def get_queryset(self):
        try:
            self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
            user = get_object_or_404(User, username=self.kwargs.get('username'))
            myarticles = Article.objects.filter(
                            web_mode=self.request.META['HTTP_HOST'],
                            author=user).order_by('-date_created')
        except:
            myarticles = Article.objects.order_by('-date_created')
            if self.tgt_url_args.get('Theme', False):
                myarticles = Article.objects.filter(
                                theme=self.tgt_url_args['Theme'],
                                web_mode=self.request.META['HTTP_HOST']).order_by('-date_created')
            else:
                myarticles = Article.objects.filter(
                                web_mode=self.request.META['HTTP_HOST']).order_by('-date_created')
        myarticles = alice().do_shorten_text(myarticles, 100, 2)
        return myarticles


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/v_article_detail.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "View Article Detail",
                    'template_name': template_name,
                    'extensions': extensions}

    def get_context_data(self, **kwargs):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    form_class = ArticleCreateForm
    template_name = 'articles/v_article_form.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Create Article",
                    'template_name': template_name,
                    'extensions': extensions}

    def get_context_data(self, *args, **kwargs):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context = super(ArticleCreateView, self).get_context_data(*args, **kwargs)
        context.update(MyHelper.get_context_metadata(self, ArticleCreateView.view_args))
        ArticleCreateView.success_url = '/'+'/'.join([key+'='+str(value) if type(value)==int else str(value) for key, value in self.tgt_url_args.items()]).replace('/add', '/view')
        return context

    def form_valid(self, form):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        form.instance.theme = self.tgt_url_args.get('Theme', '0')
        form.instance.author = self.request.user
        form.instance.web_mode = self.request.META['HTTP_HOST']
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'articles/v_article_form.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Update Article",
                    'template_name': template_name,
                    'extensions': extensions}

    def get_context_data(self, **kwargs):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        ArticleUpdateView.success_url = '/'+'/'.join([key+'='+str(value) if type(value)==int else str(value) for key, value in self.tgt_url_args.items()]).replace('/change', '/view')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.web_mode = self.request.META['HTTP_HOST']
        return super().form_valid(form)

    def test_func(self):
        Article = self.get_object()
        if self.request.user == Article.author:
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/v_article_confirm_delete.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Delete Article",
                    'template_name': template_name,
                    'extensions': extensions}

    def get_context_data(self, **kwargs):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        self.tgt_url_args['Article'] = 0
        ArticleDeleteView.success_url = '/'+'/'.join([key+'='+str(value) if type(value)==int else str(value) for key, value in self.tgt_url_args.items()]).replace('/delete', '/view')
        #print(f'success url: {ArticleDeleteView.success_url}')
        return context

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False

"""
    home views taken back home
"""
class UserThemeListView(ListView):
    model = Theme
    template_name = 'blog/v_body_1.html'
    extensions = ['blog/base.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Überblick",
                    'template_name': template_name,
                    'extensions': extensions}
    context_object_name = 'themes'

    def get_context_data(self, **kwargs):
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        return context

    def get_queryset(self):
        try:
            self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
            user = get_object_or_404(User, username=self.kwargs.get('username'))
            queryset = Theme.objects.filter(
                            web_mode=self.request.META['HTTP_HOST'],
                            author=user).order_by('-importance')
        except:
            queryset = Theme.objects.filter(
                            web_mode=self.request.META['HTTP_HOST']).order_by('-importance')
        queryset = alice().do_shorten_text(queryset, 100, 2)
        return queryset

def about(request):
    return render(request, 'blog/v_about.html', {'title': 'about'})

