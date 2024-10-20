from django.contrib import admin
from .models import Category, Product, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    ordering = ('-price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'order_date')
    list_filter = ('user', 'order_date')
    search_fields = ('user__username', 'products__name')
    readonly_fields = ('total_price', 'order_date')
    ordering = ('-order_date',)

    filter_horizontal = ('products',)  
