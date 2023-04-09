
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from news.models import PostCategory, Post, Author, User
from news.tasks import send_notification





@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        for category in categories:
            category_id = category.pk

        send_notification.delay(instance.pk, category_id)

@receiver(pre_save, sender=Post)
def presave_verify(sender, instance, **kwargs):
    author_id = instance.author_id
    posts_in_day = Post.objects.all().filter(author=Author.objects.get(id=author_id), time_in__gt=datetime.now()-timedelta(hours=24))
    if len(posts_in_day)>7:
        raise Exception("Вы превысили количество создаваемых статей в день")