from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,
    DeleteView, TemplateView,
)
from .models import Post, Category
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.change_post')
    template_name = 'post_edit.html'



class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    permission_required = ('news.delete_post')
    success_url = reverse_lazy('post_list')



class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(content = 'NW')
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewsSearch(LoginRequiredMixin, ListView):
    model = Post
    queryset = Post.objects.filter(content='NW')
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'post_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.add_post')
    template_name = 'post_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content = 'NW'
        self.object.save()
        return super().form_valid(form)




class ArticlesList(ListView):
    model = Post
    queryset = Post.objects.filter(content = 'AC')
    ordering = '-time_in'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context



class ArticlesSearch(LoginRequiredMixin, ListView):
    model = Post
    queryset = Post.objects.filter(content='AC')
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'post_search'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.add_post')
    template_name = 'post_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content = 'AC'
        self.object.save()
        return super().form_valid(form)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'author').exists()
        return context



@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = "Вы подписаны на категорию новостей"
    return render(request,'subscribe.html', {'category':category.subject, 'message':message})
