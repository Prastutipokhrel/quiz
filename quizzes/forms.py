# forms.py
from django import forms
from .models import Problem, Quiz, SubCategory


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['sub_category', 'question_text_template', 'correct_answer']


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'problems']
        widgets = {
            'problems': forms.CheckboxSelectMultiple(),
        }
