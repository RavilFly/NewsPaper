from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime
from .models import Post, Category


@shared_task
def send_notification(post_id, category_id):
    category = Category.objects.get(pk=category_id)

    subscribers = []
    subscribers += category.subscribers.all()
    subscribers = [s.email for s in subscribers]

    send_mail(
        subject = f'{Post.objects.get(pk=post_id).title}',
        message = f'{Post.objects.get(pk=post_id).content_text}',
        from_email = 'rawil-m@yandex.ru',
        recipient_list = subscribers,
    )


@shared_task
def send_weekly_newslist():

    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__subject', flat=True))
    subscribers = set(Category.objects.filter(subject__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject = 'Статьи за неделю.',
        body = '',
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
