# forms.py

from django import forms
from .models import Category, SubCategory, Problem
from django.forms import inlineformset_factory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']




# class ProblemForm(forms.ModelForm):
#     class Meta:
#         model = Problem
#         fields = [ 'question_text','math_text','correct_answer','subcategory']
#         widgets = {
#             'math_text': forms.HiddenInput(),
#         }

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['question_text','correct_option','correct_formula', 'subcategory']

# Inline formsets
SubCategoryFormSet = inlineformset_factory(Category, SubCategory, form=SubCategoryForm, extra=1)
ProblemFormSet = inlineformset_factory(SubCategory, Problem, form=ProblemForm, extra=1)
