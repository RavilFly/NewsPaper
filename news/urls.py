from django.urls import path
from .views import (
    PostsList, PostDetail, PostDelete, PostUpdate,
    NewsList, NewsSearch, NewsCreate,
    ArticlesList, ArticleCreate, ArticlesSearch,
)

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path("news/", NewsList.as_view(), name='news_list'),
    path('news/search/', NewsSearch.as_view()),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/', ArticlesList.as_view(), name='articles_list'),
    path('articles/search/', ArticlesSearch.as_view()),
    path('articles/<int:pk>', PostDetail.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),

]