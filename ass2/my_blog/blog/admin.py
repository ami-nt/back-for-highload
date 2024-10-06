from django.contrib import admin
from .models import Post, UserProfile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'created_at', 'get_tags']
    search_fields = ['title']

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'
    
@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']




