# admin.py

from django.contrib import admin
from .models import Category, SubCategory, Problem, Role, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'correct_formula', 'subcategory')
    list_filter = ('subcategory',)
    search_fields = ('question_text', 'subcategory__name')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'role__name')
