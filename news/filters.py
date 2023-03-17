from django_filters import FilterSet, DateTimeFilter
from django import forms
from .models import Post

class PostFilter(FilterSet):
    time_in = DateTimeFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gt',
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author_id__user_relation_id': ['exact'],
            #'time_in':['year__gt'],

        }
        labels = {
            'title' : 'Заголовок',
            #'author_id': 'Автор',
            #'time_in': 'Время публикации',
            # 'category': 'Категория',
        }
