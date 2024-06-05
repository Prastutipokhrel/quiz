from .models import Category, SubCategory, Quiz, Problem, Role, UserProfile
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProblemForm, QuizForm

import random


# Create your views here.

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        roles = Role.objects.all()
        if form.is_valid():
            user = form.save()
            selected_role_id = request.POST.get('role')
            selected_role = Role.objects.get(id=selected_role_id)
            UserProfile.objects.create(user=user, role=selected_role)
            login(request, user)
            return redirect('quiz:home')
    else:
        form = UserCreationForm()
        roles = Role.objects.all()
    return render(request, 'user/register.html', {'form': form, 'roles': roles})


# Home view to redirect users based on their roles
@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    print(user_profile.role.name)
    if user_profile.role.name == 'Student':
        return redirect('quiz:student_view')
    elif user_profile.role.name == 'Teacher':
        return redirect('quiz:teacher_view')
    elif user_profile.role.name == 'Editor':
        return redirect('quiz:editor_view')
    else:
        return redirect('quiz:login')


# Role-based views
@login_required
def student_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    print(user_profile.role.name)
    if user_profile.role.name == 'Student':
        return render(request, 'user/student.html')
    else:
        return redirect('quiz:home')


@login_required
def teacher_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role.name == 'Teacher':
        return render(request, 'user/teacher.html')
    else:
        return redirect('quiz:home')


@login_required
def editor_view(request):
    problems = Problem.objects.all()
    quizzes = Quiz.objects.all()
    return render(request, 'user/editor/editor_view.html',
                  {'problems': problems, 'quizzes': quizzes})


@login_required
def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz:editor_view')
    else:
        form = ProblemForm()
    return render(request, 'user/editor/problem_form.html', {'form': form})


@login_required
def edit_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect('quiz:editor_view')
    else:
        form = ProblemForm(instance=problem)
    return render(request, 'user/editor/problem_form.html', {'form': form})


@login_required
def delete_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    if request.method == 'POST':
        problem.delete()
        return redirect('quiz:editor_view')
    return render(request, 'user/editor/problem_confirm_delete.html', {'problem': problem})


@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            form.save_m2m()
            return redirect('quiz:editor_view')
    else:
        form = QuizForm()
    return render(request, 'user/editor/quiz_form.html', {'form': form})


@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz:editor_view')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'user/editor/quiz_form.html', {'form': form})


@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz:editor_view')
    return render(request, 'user/editor/quiz_confirm_delete.html', {'quiz': quiz})


@login_required
def start_page(request):
    return render(request, 'start.html')


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

@login_required
def quiz_get(request):
    user = request.user
    user_role = request.user.userprofile.role

    question_number = request.session.get('question_number', 1)
    score = request.session.get('score', 0)

    total_questions = 5

    if question_number > total_questions:
        return render(request, 'end.html', {'score': score, 'q_no': question_number - 1})

    # Determine the number of problems in the Problem model
    problems_count = Problem.objects.count()

    if question_number <= problems_count:
        problem = Problem.objects.all()[question_number - 1]
        context = {
            'question': problem.question_text_template,
            'correct_answer': problem.correct_answer,
            'question_type': 'true_false',
            'question_number': question_number,
            'score': score,
        }
        request.session['current_problem_id'] = problem.id
    else:
        # If no more problems, consider it the end of quiz
        return render(request, 'end.html', {'score': score, 'q_no': question_number - 1})

    request.session['question_type'] = 'true_false'
    return render(request, 'list.html', context, {'user': user, 'role': user_role})


@login_required
def quiz_post(request):
    question_number = request.session.get('question_number', 1)
    score = request.session.get('score', 0)
    question_type = request.session.get('question_type')

    if question_type == 'true_false':
        current_id = request.session.get('current_problem_id')
        problem = Problem.objects.get(id=current_id)
        answer = request.POST['selected_answer']
        if f'{answer}' == f'{problem.correct_answer}':
            score += 1

    request.session['score'] = score
    request.session['question_number'] = question_number + 1

    return redirect('quiz:quiz_get')


@login_required
def next_question(request):
    question_number = request.session.get('question_number', 0)
    request.session['question_number'] = question_number + 1
    return redirect('quiz:quiz_get')


@login_required
def reset_quiz(request):
    request.session['question_number'] = 1
    request.session['score'] = 0
    request.session['question_type'] = None
    return redirect('quiz:quiz_get')
