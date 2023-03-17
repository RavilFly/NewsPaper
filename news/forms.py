from django import forms
from django.core.exceptions import ValidationError
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        content = 'NW'
        model = Post
        fields = [
            'title',
            'author',
            'category',
            'content_text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is None:
            raise ValidationError({
                'title' : 'Укажите понятный заголовок.'
            })

        content_text = cleaned_data.get('content_text')
        if content_text == title:
            raise ValidationError({
                'content_text' : 'Заголовок совпадает с текстом'
            })
        if len(content_text) < 30:
            raise ValidationError({
                'content_text' : 'Пишите более подробный текст.'
            })


        return cleaned_data
