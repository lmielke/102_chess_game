from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Post, Article
from .forms import PostCreateForm
import os
from web_project.alice import alice
from web_project.helper import MyHelper


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/v_posts.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Überblick",
                    'template_name': template_name,
                    'extensions': extensions
                    }
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        return context

    def get_queryset(self):
        try:
            self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
            user = get_object_or_404(User, username=self.kwargs.get('username'))
            if self.tgt_url_args.get('Article', '0') != 0:
                posts = Post.objects.filter(
                            web_mode=self.request.META['HTTP_HOST'],
                            author=user,
                            article_field=self.tgt_url_args['Article']).order_by('-date_created')
            else:
                posts = Post.objects.filter(
                            web_mode=self.request.META['HTTP_HOST'],
                            author=user).order_by('-date_created')
        except:
            if self.tgt_url_args.get('Article', '0') != 0:
                posts = Post.objects.filter(
                            web_mode=self.request.META['HTTP_HOST'],
                            article_field=self.tgt_url_args['Article']).order_by('-date_created')
            else:
                posts = Post.objects.order_by('-date_created')
                posts = Post.objects.filter(
                            web_mode=self.request.META['HTTP_HOST']).order_by('-date_created')
        return posts


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/v_post_detail.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "View Post Detail",
                    'template_name': template_name,
                    'extensions': extensions
                    }

    def get_context_data(self, **kwargs):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = 'blog/v_post_form.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Create Post",
                    'template_name': template_name,
                    'extensions': extensions
                    }

    def get_context_data(self, *args, **kwargs):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        del self.tgt_url_args['Post']
        PostCreateView.success_url = '/'+'/'.join([key+'='+str(value) if type(value)==int else str(value) for key, value in self.tgt_url_args.items()]).replace('posts', 'articles').replace('/add', '/view')
        return context

    def form_valid(self, form):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        form.instance.theme = self.tgt_url_args.get('Theme', '0')
        form.instance.author = self.request.user
        form.instance.web_mode = self.request.META['HTTP_HOST']
        blog_article = Article.objects.get(pk=self.tgt_url_args.get('Article', '0'))
        form.instance.article_field = blog_article
        messages.success(self.request, 'Vielen Dank für Ihren Kommentar!')
        print(f"in block views made it here")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    counter = 0
    form_class = PostCreateForm
    template_name = 'blog/v_post_form.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Update Post",
                    'template_name': template_name,
                    'extensions': extensions
                    }

    def get_context_data(self, **kwargs):
        print(f'get_context_data: {self.counter}')
        self.counter += 1
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        del self.tgt_url_args['Post']
        PostUpdateView.success_url = '/'+'/'.join([key+'='+str(value) if type(value)==int else str(value) for key, value in self.tgt_url_args.items()]).replace('/change', '/view')
        print(f'success url: {PostUpdateView.success_url}')
        return context

    def form_valid(self, form):
        print(f'form_valid: {self.counter}')
        self.counter += 1
        form.instance.author = self.request.user
        form.instance.web_mode = self.request.META['HTTP_HOST']
        return super().form_valid(form)

    def test_func(self):
        print(f'test_func: {self.counter}')
        self.counter += 1
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/v_post_confirm_delete.html'
    extensions = ['blog/body.html', 'blog/base_iframe.html']
    view_args = {'page_title': "Delete Post",
                    'template_name': template_name,
                    'extensions': extensions
                    }

    def get_context_data(self, **kwargs):
        self.tgt_url_args = MyHelper.parse_tgt_url(self, self.request.path_info)
        context = (super().get_context_data(**kwargs))
        context.update(MyHelper.get_context_metadata(self, self.view_args))
        del self.tgt_url_args['Post']
        PostDeleteView.success_url = '/'+'/'.join([key+'='+str(value) if type(value)==int else str(value) for key, value in self.tgt_url_args.items()]).replace('/delete', '/view')
        #print(f'success url: {PostDeleteView.success_url}')
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
