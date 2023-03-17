from django import forms
from django.core.exceptions import ValidationError
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author_id',
            'time_in',
            #'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError({
                'title' : 'Укажите понятный заголовок.'
            })
        return cleaned_data