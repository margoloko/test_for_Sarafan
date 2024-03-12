from django.contrib import admin

from .models import Category, SubCategory, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Category."""
    
    list_display = ("name", "slug",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Админка для модели SubCategory."""
    
    list_display = ("name", "slug", "category")
    list_filter = ("name", "category")
    search_fields = ("name", "category")
    ordering = ("name", "category")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для модели Product."""
    
    list_display = ("name", "slug", "price", "subcategory")
    list_filter = ("name", "price", "subcategory")
    search_fields = ("name", "price", "subcategory")
    ordering = ("name", "price", "subcategory",)
