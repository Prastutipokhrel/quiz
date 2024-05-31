from django.shortcuts import render

# Create your views here.
from .models import Question , EquationQuestion
from django.http import Http404
from django.http import JsonResponse
from .utils import generate_equation
import random


# def start_page(request):
#     return render(request, 'start.html')
# from django.shortcuts import render, redirect
# from .models import Question

# def quiz_get(request):
#     question_number = request.session.get('question_number', 0)
#     score = request.session.get('score', 0)
#     # feedback = request.session.get('feedback', None)
#     print(question_number)
#     print(score)
#     # Checking if all questions have been answered
#     if question_number >= Question.objects.count():
#         return render(request, 'end.html', {'score': score, 'q_no':question_number})

#     # Fetching the current question
#     question = Question.objects.all()[question_number]
#     context = {
#         'question': question
#     }
#     print(context)

#     return render(request, 'list.html', context)

# def quiz_post(request):
#     question_number = request.session.get('question_number', 0)
#     score = request.session.get('score', 0)

#     # Fetch the current question
#     question = Question.objects.all()[question_number]

#     if request.method == 'POST':
#         answer = request.POST['selected_answer']
#         print(answer)
#         # Update the score based on the submitted answer
#         print(question.correct_answer)
#         if f'{answer}' == f'{question.correct_answer}':
#             request.session['score'] = score + 1

#         # Update the question number for the next question
#         request.session['question_number'] = question_number + 1
#         # Redirect to the GET view to show the next question
#         return redirect('quiz:quiz_get')
#     else:
#         # If not a POST request, redirect to the GET view
#         return redirect('quiz:quiz_get')

# def next_question(request):
#     question_number = request.session.get('question_number', 0)
#     # Update the question number for the next question
#     request.session['question_number'] = question_number + 1
#     return redirect('quiz:quiz_get')


# def reset_quiz(request):
#     request.session['question_number'] = 0
#     request.session['score'] = 0
#     request.session['feedback'] = None
#     return redirect('quiz:quiz_get')

#equation views

def quiz_get(request):
    question_number = request.session.get('question_number', 0)
    score = request.session.get('score', 0)
    feedback = request.session.get('feedback', None)
    question_type = request.session.get('question_type', None)

    # Check if maximum questions limit is reached
    if question_number >= 10:
        return render(request, 'end.html', {'score': score, 'q_no': question_number})

    if feedback:
        context = {
            'feedback': feedback,
            'question_type': question_type,
            'show_next': True
        }
        return render(request, 'list.html', context)

    # Determine question type
    if random.choice([True, False]):
        # Handle true/false question
        if question_number < Question.objects.count():
            question = Question.objects.all()[question_number]
            context = {
                'question': question,
                'question_type': 'true_false'
            }
            request.session['question_type'] = 'true_false'
        else:
            return render(request, 'end.html', {'score': score, 'q_no': question_number})
    else:
        # Handle equation question
        equation_data = Equation.generate_equation()
        request.session['current_equation'] = equation_data
        formatted_equation = f"{equation_data['coefficient']}*x + {equation_data['constant']} = {equation_data['solution'] + equation_data['constant']}"
        context = {
            'equation': formatted_equation,
            'question_type': 'equation'
        }
        request.session['question_type'] = 'equation'

    request.session['feedback'] = None
    return render(request, 'list.html', context)

def quiz_post(request):
    question_number = request.session.get('question_number', 0)
    score = request.session.get('score', 0)
    question_type = request.session.get('question_type')

    if question_type == 'equation':
        # Handle equation question
        answer = int(request.POST['answer'])
        equation_data = request.session.get('current_equation')
        correct_answer = equation_data['solution']
        if answer == correct_answer:
            request.session['score'] = score + 1
            feedback = "Correct!"
        else:
            feedback = "Incorrect!"
    else:
        # Handle true/false question
        question = Question.objects.all()[question_number]
        answer = request.POST['selected_answer']
        if f'{answer}' == f'{question.correct_answer}':
            request.session['score'] = score + 1
            feedback = "Correct!"
        else:
            feedback = "Incorrect!"

    request.session['feedback'] = feedback
    return redirect('quiz:quiz_get')

def next_question(request):
    question_number = request.session.get('question_number', 0)
    request.session['question_number'] = question_number + 1
    return redirect('quiz:quiz_get')

def reset_quiz(request):
    request.session['question_number'] = 0
    request.session['score'] = 0
    request.session['feedback'] = None
    request.session['question_type'] = None
    return redirect('quiz:quiz_get')


