from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views import View
from .models import Post,Comment
from .forms import PostForm,CommentForm, RegisterForm, LoginForm
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login


def hello_blog(request):
    return HttpResponse("Hello, Blog!")


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})
    
    
def post_detail(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No post")
    
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})
    
    
def create_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False) 
        post.author = request.user  
        post.save()  
        return HttpResponseRedirect("/posts/")
    return render(request, 'form.html', {'form': form})

          
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
            return HttpResponseRedirect("/posts/")
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
        return HttpResponseRedirect("/posts/")

    
class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login/")
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
                    return HttpResponseRedirect("/posts/")
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        return render(request, 'login.html', {'form': form})