from .models import Category, SubCategory, Quiz, Problem, Role, UserProfile , StudentProgress
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, SubCategoryFormSet, ProblemFormSet , ProblemForm , SubCategoryForm

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
        categories = Category.objects.all().order_by('name')
        print(categories)
        context = {
            'categories': categories,
        }
        return render(request, 'user/student/category.html',context)
    else:
        return redirect('quiz:home')

@login_required
def student_subcategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = SubCategory.objects.filter(category=category)
    completed_subcategories = []

    for subcategory in subcategories:
        total_problems = subcategory.problems.count()
        mastered_problems = StudentProgress.objects.filter(user=request.user, subcategory=subcategory, mastered=True).count()

        if total_problems == mastered_problems and total_problems > 0:
            completed_subcategories.append(subcategory.id)

    context = {
        'category': category,
        'subcategories': subcategories,
        'completed_subcategories': completed_subcategories,
    }
    return render(request, 'user/student/subcategory.html', context)



from django.http import JsonResponse

@login_required
def student_problem(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    problems = Problem.objects.filter(subcategory=subcategory)

    if not problems.exists():
        return redirect('quiz:home')

    # Initialize session variables if not already set
    if 'current_problem_index' not in request.session:
        request.session['current_problem_index'] = 0
        request.session['correct_streak'] = 0
        request.session['incorrect_streak'] = 0

    current_index = request.session['current_problem_index']

    # Find the next unmastered problem
    problems_list = list(problems)
    for i in range(len(problems_list)):
        problem_index = (current_index + i) % len(problems_list)
        problem = problems_list[problem_index]
        studentprogress = StudentProgress.objects.filter(user=request.user, problem=problem).first()
        if not studentprogress or not studentprogress.mastered:
            request.session['current_problem_index'] = problem_index
            break
    else:
        # All problems have been mastered
        context = {
            'all_mastered': True,
        }
        return render(request, 'user/student/quiz_problem.html', context)

    question_text, correct_answer, params = problem.generate_dynamic_problem()

    if request.method == 'POST':
        if 'next_problem' in request.POST:
            request.session['current_problem_index'] = (current_index + 1) % len(problems_list)
            return redirect('quiz:student_problem', subcategory_id=subcategory_id)

        user_answer = request.POST.get('selected_answer')
        if user_answer == str(problem.correct_option):
            request.session['correct_streak'] += 1
            request.session['incorrect_streak'] = 0
            if request.session['correct_streak'] == 2:
                user = request.user
                student_progress, created = StudentProgress.objects.get_or_create(
                    user=user,
                    problem=problem,
                    subcategory=subcategory,
                )
                student_progress.mastered = True
                student_progress.save()
                request.session['correct_streak'] = 0
                context = {
                    'question_text': question_text,
                    'problem_id': problem.id,
                    'subcategory_id': subcategory_id,
                    'studentprogress': True,
                    'all_mastered': False,
                    'correct_formula': None,
                    'disable_submit': False,
                    'mastered': True
                }
                return render(request, 'user/student/quiz_problem.html', context)
        else:
            request.session['correct_streak'] = 0
            request.session['incorrect_streak'] += 1
            if request.session['incorrect_streak'] == 2:
                request.session['incorrect_streak'] = 0
                context = {
                    'question_text': question_text,
                    'problem_id': problem.id,
                    'subcategory_id': subcategory_id,
                    'studentprogress': False,
                    'all_mastered': False,
                    'correct_formula': problem.correct_formula,
                    'disable_submit': True,
                    'correct_option':problem.correct_option,

                    
                }
                return render(request, 'user/student/quiz_problem.html', context)
        return redirect('quiz:student_problem', subcategory_id=subcategory_id)
    
    context = {
        'question_text': question_text,
        'problem_id': problem.id,
        'subcategory_id': subcategory_id,
        'studentprogress': False,
        'all_mastered': False,
        'correct_formula': None,
        'disable_submit': False,
        'mastered': False,
        'correct_option':problem.correct_option,
    }

    return render(request, 'user/student/quiz_problem.html', context)



@login_required
def teacher_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role.name == 'Teacher':
        return render(request, 'user/teacher.html')
    else:
        return redirect('quiz:home')


@login_required
def editor_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'user/editor/editor_view.html', context)

@login_required
def subcategory_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    print(category)
    subcategories = SubCategory.objects.filter(category=category)
    context = {
        'category': category,
        'subcategories': subcategories,
    }
    return render(request, 'user/editor/subcategory_view.html', context)




@login_required
def manage_category(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
    else:
        category = Category()

    if request.method == 'POST':
        category_form = CategoryForm(request.POST, instance=category)
        subcategory_formset = SubCategoryFormSet(request.POST, instance=category)

        if category_form.is_valid() and subcategory_formset.is_valid():
            category_form.save()
            subcategory_formset.save()
            return redirect('quiz:editor_view')
    else:
        category_form = CategoryForm(instance=category)
        subcategory_formset = SubCategoryFormSet(instance=category)

    return render(request, 'user/editor/manage_category.html', {
        'category_form': category_form,
        'subcategory_formset': subcategory_formset,
    })


@login_required

def manage_subcategory(request, category_id):
    print(category_id)
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        subcategory_form = SubCategoryForm(request.POST)
        if subcategory_form.is_valid():
            subcategory = subcategory_form.save(commit=False)
            subcategory.category = category  # Assign category to the subcategory
            subcategory.save()
            return redirect('quiz:subcategory_detail', subcategory_id=subcategory.id)
    else:
        subcategory_form = SubCategoryForm()

    return render(request, 'user/editor/manage_subcategory.html', {
        'subcategory_form': subcategory_form,
        'category': category,
    })


@login_required

def manage_problem(request, subcategory_id):
    subcategory = SubCategory.objects.get(id=subcategory_id)
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.subcategory = subcategory
            problem.save()
            if request.POST.get('action') == 'add_another':
                print("Problem saved successfully. Redirecting to manage_problem view.")
                return redirect('quiz:manage_problem', subcategory_id=subcategory.id)
            else:
                print("Problem saved successfully. Redirecting to subcategory_detail view.")
                return redirect('quiz:subcategory_detail', subcategory_id=subcategory.id)
        else:
            print("Form is not valid. Errors: %s", form.errors)
    else:
        form = ProblemForm()
        
    return render(request, 'user/editor/manage_problem.html', {'form': form, 'subcategory': subcategory})

@login_required
def add_problem(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.subcategory = subcategory
            problem.save()
            if request.POST.get('action') == 'done':
                return redirect('quiz:subcategory_detail',subcategory_id=subcategory_id)  # Redirect to a relevant page after saving
            else:
                return redirect('add_problem', subcategory_id=subcategory_id)
    else:
        form = ProblemForm()
    
    context = {
        'form': form,
        'subcategory': subcategory,
    }
    return render(request, 'user/editor/add_problem.html', context)

@login_required
def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    problems = Problem.objects.filter(subcategory=subcategory).values('id','question_text','correct_formula','correct_option')
    print(problems)
    return render(request, 'user/editor/subcategory_detail.html', {
        'subcategory': subcategory,
        'problems': list(problems),
    })

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('quiz:editor_view')


@login_required
def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    category_id = subcategory.category.id
    subcategory.delete()
    return redirect('quiz:category_detail', category_id=category_id)


@login_required
def delete_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    subcategory_id = problem.subcategory.id
    problem.delete()
    return redirect('quiz:subcategory_detail', subcategory_id=subcategory_id)

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz:editor_view')
    return render(request, 'user/subcategory_view/quiz_confirm_delete.html', {'quiz': quiz})


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
