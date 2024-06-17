from django.db import models
from django.conf import settings
import random ,re
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

import random
import re
from django.db import models
import string

class Problem(models.Model):
    question_text = models.CharField(default='', max_length=255)  # Template for the problem
    correct_formula = models.CharField(default='', max_length=255)  # Formula for the correct answer
    correct_option = models.BooleanField(choices=[(True, 'True'), (False, 'False')], default=True)

    subcategory = models.ForeignKey('SubCategory', related_name='problems', on_delete=models.CASCADE)

    def generate_dynamic_problem(self):
        # Step 1: Define the parameters
        params = {
            'p1': random.randint(-10, 10),
            'p2': random.randint(-10, 10),
            'p3': random.randint(-10, 10),
            'p4': random.choice(string.ascii_letters),
        }

        # Print params to verify
        print("Generated parameters:", params)

        # Step 2: Define the original string
        original_string = self.question_text

        # Step 3: Dynamically replace all placeholders with their values
        def replace_params(string_template, parameters):
            for key, value in parameters.items():
                string_template = string_template.replace(key, f'({value})')
            return string_template
        
        question_template = replace_params(original_string, params)

        def multiply_with_params(string_template):
            # Regex to match numbers followed by * and parameter (e.g., 2*p1)
            def multiply(match):
                number = int(match.group(1))
                param_value = int(match.group(2))
                return str(number * param_value)
            
            pattern = re.compile(r'(\d+)\*\((\-?\d+)\)')
            string_template = re.sub(pattern, multiply, string_template)
            return string_template

        # Apply the multiplication
        question_template = multiply_with_params(question_template)
        print(question_template)
        
        # Function to handle the replacement of squared and cubed numbers
        def replace_power_numbers(match):
            base = int(match.group(1))  # Extract the number
            exponent = int(match.group(2))  # Extract the exponent
            power_number = base ** exponent  # Compute the power
            return str(power_number)  # Return the power number as a string

        # Replace squared and cubed numbers in the question_template
        question_template = re.sub(r'(\-?\d+)\^([2-3])', replace_power_numbers, question_template)
        print(question_template)
        # Function to handle multiplication with parameters
        def multiply_with_params(string_template):
        # Regex to match numbers followed by * and parameter (e.g., 2*p1)
            def multiply(match):
                number = int(match.group(1))
                param_value = int(match.group(2))
                return str(number * param_value)
        
            pattern = re.compile(r'(\d+)\*\((\-?\d+)\)')
            string_template = re.sub(pattern, multiply, string_template)
            return string_template

        # Apply the multiplication
        question_template = multiply_with_params(question_template)

        # Function to handle double negatives and '- +' patterns
        def handle_signs(string):
            string = re.sub(r'\(\-', '-', string)  # Replace '(-' with '-'
            string = re.sub(r'\-\+', '-', string)  # Replace '-+' with '-'
            string = re.sub(r'\+\-', '-', string)  # Replace '+-' with '-'
            string = re.sub(r'\-\-', '+', string)  # Replace '--' with '+'
            string = re.sub(r'\(\+', '(', string)  # Replace '(+' with '('
            return string
        
        question_template = handle_signs(question_template)
        print("Processed question template:")
        print(question_template)

        # Generate the correct answer using the correct_formula and params
        correct_answer = self.correct_formula

        return question_template, correct_answer, params



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

class StudentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    subcategory= models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    mastered = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_id', 'problem_id', 'subcategory_id')