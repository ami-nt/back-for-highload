from django.urls import path, include
from django.conf import settings
from .views import UserListView, UserDetailView, ProductListCreateView, ProductDetailView, OrderListCreateView, OrderDetailView, CategoryListCreateView, CategoryDetailView, CachedProductListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import debug_toolbar

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
     path('cached-products/', CachedProductListView.as_view(), name='cache-product-list-create'),

    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),  
    ] + urlpatterns
