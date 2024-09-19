from django.urls import path
from .views import hello_blog, post_list, post_detail, create_post, PostEditView, PostDelView, RegisterView, LoginView
from django.contrib.auth import views as auth_views  

urlpatterns = [
    path('hello_blog/', hello_blog),
    path('posts/', post_list, name="post_list"),
    path("posts/new/",  create_post, name='post_new'),
    path('posts/<int:id>', post_detail, name='post_by_id'),
    path('posts<int:id>/edit/',  PostEditView.as_view(), name="post_edit"),
    path("posts/<int:id>/delete/", PostDelView.as_view(), name="delete"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]