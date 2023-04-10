from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    PostsList, PostDetail, PostDelete, PostUpdate,
    NewsList, NewsSearch, NewsCreate,
    ArticlesList, ArticleCreate, ArticlesSearch,
    CategoryListView, subscribe
)

urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path("news/", cache_page(300)(NewsList.as_view()), name='news_list'),
    path('news/search/', NewsSearch.as_view()),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/', cache_page(300)(ArticlesList.as_view()), name='articles_list'),
    path('articles/search/', ArticlesSearch.as_view()),
    path('articles/<int:pk>', PostDetail.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('news/categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('news/categories/<int:pk>/subscribe', subscribe, name = 'subscribe'),
]