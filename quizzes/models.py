from django.db import models
from django.conf import settings
import random

class Question(models.Model):
    question_text = models.CharField(max_length=500)
    TRUE_FALSE_CHOICES = (
        (True, 'True'),
        (False, 'False'),
    )
    correct_answer = models.BooleanField(choices=TRUE_FALSE_CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_questions',
    )

class EquationQuestion(models.Model):
    parameter1 = models.IntegerField()
    parameter2 = models.IntegerField()
    parameter3 = models.IntegerField()
    correct_answer = models.FloatField()
    question_text = models.CharField(max_length=500)

    @staticmethod
    def generate_equation():
        p1 = random.randint(-10, 10)
        p2 = random.randint(-10, 10)
        p3 = random.randint(-10, 10)
        question_text = f"{p1} * x + {p2} = {p3}"
        correct_answer = (p3 - p2) / p1
        return EquationQuestion(parameter1=p1, 
        parameter2=p2, 
        parameter3=p3,
        question_text=question_text,
        correct_answer=correct_answer)