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

class Equation(models.Model):
    coefficient = models.IntegerField()
    constant = models.IntegerField()
    solution = models.IntegerField()

    @classmethod
    def generate_equation():
        coefficient = random.randint(-10, 10)
        while coefficient == 0:  # Ensuring coefficient is not zero
            coefficient = random.randint(-10, 10)
        constant = random.randint(-10, 10)
        solution = random.randint(-10, 10)
        return {
            'coefficient': coefficient,
            'constant': constant,
            'solution': solution
        }

    def __str__(self):
        return f"{self.coefficient}*x + {self.constant} = {self.solution + self.constant}"