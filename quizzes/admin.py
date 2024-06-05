from django.contrib import admin
from .models import Category, SubCategory, Problem, Role, UserProfile


# class SubCategoryInline(admin.TabularInline):
#     model = SubCategory
#     extra = 1
#
#
# class ProblemInline(admin.TabularInline):
#     model = Problem
#     extra = 1
#
#
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     inlines = [SubCategoryInline]
#
#
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category')
#     list_filter = ('category',)
#     inlines = [ProblemInline]
#
#
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('question_text_template', 'correct_answer', 'subcategory')
    list_filter = ('subcategory',)
#
#
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#
#
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role')
#     list_filter = ('role',)


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Problem)
admin.site.register(Role)
admin.site.register(UserProfile)
