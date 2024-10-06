from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Prefetch
from django.views import View
from .models import Post, Comment, User, Tag
from .forms import LoginForm, PostForm, CommentForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

def get_posts_with_comments():
    posts = Post.objects.prefetch_related(
        Prefetch('comment_set', queryset=Comment.objects.select_related('author'))
    ).all()
    return posts


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()  
           
            tags_data = form.cleaned_data.get('tags')  
            if tags_data:
                tags = [tag.strip() for tag in tags_data.split(',')]
                for tag_name in tags:
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        post.tags.add(tag)  
            return redirect('post_list')  
    else:
        form = PostForm()

    return render(request, 'form.html', {'form': form})


@cache_page(60) 
def post_list(request):
    posts = Post.objects.prefetch_related('comments').all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})


def post_detail(request, id):
    post = get_object_or_404(Post.objects.prefetch_related('comments'), id=id)
    comments_count = cache.get(f'comments_count_{post.id}')
    
    if comments_count is None:
        comments_count = post.comments.count()  
        cache.set(f'comments_count_{post.id}', comments_count, timeout=60) 
    
    comments = post.comments.all().order_by('-created_at')
    # Amangeldi Amina
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post 
            comment.author = request.user  
            comment.save()  
            cache.delete(f'comments_count_{post.id}')
            return redirect('post_by_id', id=post.id)  
    else:
        form = CommentForm()
        
    return render(request, 'post_id.html', {'post': post, 'comments': comments, 'form': form, 'comments_count': comments_count})


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect("/blog/login/")
        else:
            print(form.errors)  
        return render(request, 'register.html', {'form': form})

    
class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            user = authenticate(username=f['username'], password=f['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/blog/posts/")
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        return render(request, 'login.html', {'form': form})
    

class PostEditView(View):
   
    def get(self, request, id):
        post = Post.objects.get(pk=id)
        if post.author != request.user.username:
            return HttpResponse("Unauthorized")
        form = PostForm(instance=post)
        user = request.user.username
        return render(request, 'edit.html', {'form': form, 'post': post, 'user': user})
    

    def post(self, request,id):
        post = Post.objects.get(pk=id)
        if post.author != request.user.username:
            return HttpResponse("Unauthorized")
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/blog/posts/")
        return render(request, 'edit.html', {'form': form, 'post': post})

    
class PostDelView(View):

    def get(self, request, id):
        post = Post.objects.get(pk=id)
        if post.author != request.user.username:
            return HttpResponse("Unauthorized")
        user = request.user.username
        return render(request, 'delete.html', {'post': post, 'user': user})
 
    def post(self, request, id):
        post = get_object_or_404(Post, pk=id)  
        if post.author != request.user.username:
            return HttpResponse("Unauthorized")
        post.delete()
        return HttpResponseRedirect("/blog/posts/")