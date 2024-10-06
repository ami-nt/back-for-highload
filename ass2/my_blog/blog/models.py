from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=250, default='No bio')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['author']), 
        ]

    def __str__(self):
        return self.title
    
# Amangeldi Amina

class Tag(models.Model):     
    name = models.CharField(max_length=30)

    class Meta:
        indexes = [
            models.Index(fields=['name']), 
        ]

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250, default='No comment')  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

# Amangeldi Amina