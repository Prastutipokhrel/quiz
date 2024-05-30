from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'user', 'correct_answer')
    search_fields = ('question_text', 'user__username')
    show_facets = admin.ShowFacets.ALWAYS
