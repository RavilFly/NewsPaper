from django.contrib import admin
from .models import Post, Category
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'title')
    list_filter = ('author',)
    search_fields = ('content', 'title',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)