from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=250, required=False, help_text='Enter tags separated by commas.')
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
