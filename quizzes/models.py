from django.db import models
from django.conf import settings
import random
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class Problem(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='problems')
    question_text_template = models.CharField(max_length=500)  # Use template for dynamic question text
    TRUE_FALSE_CHOICES = (
        (True, 'True'),
        (False, 'False'),
    )
    correct_answer = models.BooleanField(choices=TRUE_FALSE_CHOICES)

    def __str__(self):
        return self.question_text_template

    def generate_question(self):
        # Implement logic to generate dynamic question text using the template
        # Example: question_text_template = "Is {{ x }} + {{ y }} equal to {{ x + y }}?"
        # Use random values for x and y
        context = {
            'x': random.randint(1, 10),
            'y': random.randint(1, 10)
        }
        question_text = self.question_text_template.format(**context)
        return question_text


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    problems = models.ManyToManyField(Problem)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
