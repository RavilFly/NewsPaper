from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from news.models import PostCategory, Post, Author, User



def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject = title,
        body = '',
        from_email = settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

@receiver(pre_save, sender=Post)
def presave_verify(sender, instance, **kwargs):
    author_id = instance.author_id
    posts_in_day = Post.objects.all().filter(author=Author.objects.get(id=author_id), time_in__gt=datetime.now()-timedelta(hours=24))
    if len(posts_in_day)>7:
        raise Exception("Вы превысили количество создаваемых статей в день")