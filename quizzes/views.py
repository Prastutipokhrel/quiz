from django.shortcuts import render

# Create your views here.
from .models import Question , EquationQuestion
from django.http import Http404
from django.http import JsonResponse
from .utils import generate_equation
import random


def start_page(request):
    return render(request, 'start.html')
from django.shortcuts import render, redirect
from .models import Question

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

    # Select question type randomly
    question_type = random.choice(['true_false', 'equation'])

    if question_type == 'true_false':
        question = Question.objects.all()[question_number]
        context = {
            'question': question,
            'question_type': 'true_false',
        }
    else:
        if 'equation_question' not in request.session:
            equation_question = EquationQuestion.generate_equation()
            equation_question.save()
            request.session['equation_question'] = equation_question.id
        else:
            equation_question_id = request.session['equation_question']
            equation_question = EquationQuestion.objects.get(id=equation_question_id)
        context = {
            'question': equation_question,
            'question_type': 'equation',
        }

    return render(request, 'list.html', context)

def quiz_post(request):
    question_number = request.session.get('question_number', 0)
    score = request.session.get('score', 0)

    if 'equation_question' in request.session:
        equation_question_id = request.session['equation_question']
        equation_question = EquationQuestion.objects.get(id=equation_question_id)
        if request.method == 'POST':
            answer = float(request.POST['answer'])
            if answer == equation_question.correct_answer:
                request.session['score'] = score + 1
        del request.session['equation_question']
    else:
        question = Question.objects.all()[question_number]
        if request.method == 'POST':
            answer = request.POST['answer'] == 'True'
            if answer == question.correct_answer:
                request.session['score'] = score + 1

    request.session['question_number'] = question_number + 1
    return redirect('quiz:quiz_get')

def next_question(request):
    question_number = request.session.get('question_number', 0)
    # Update the question number for the next question
    request.session['question_number'] = question_number + 1
    return redirect('quiz:quiz_get')

def reset_quiz(request):
    request.session['question_number'] = 0
    request.session['score'] = 0
    if 'equation_question' in request.session:
        del request.session['equation_question']
    return redirect('quiz:quiz_get')


