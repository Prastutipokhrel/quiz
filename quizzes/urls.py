from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'quiz'
urlpatterns = [
    # quiz views
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('student', views.student_view, name='student_view'),
    path('teacher', views.teacher_view, name='teacher_view'),
    path('editor', views.editor_view, name='editor_view'),
    path('quiz_get', views.quiz_get, name='quiz_get'),
    path('submit', views.quiz_post, name='quiz_post'),
    path('next', views.next_question, name='next_question'),
    path('reset', views.reset_quiz, name='reset_quiz'),

    path('editor/', views.editor_view, name='editor_view'),
    path('editor/create_problem/', views.create_problem, name='create_problem'),
    path('editor/edit_problem/<int:problem_id>/', views.edit_problem, name='edit_problem'),
    path('editor/delete_problem/<int:problem_id>/', views.delete_problem, name='delete_problem'),
    path('editor/create_quiz/', views.create_quiz, name='create_quiz'),
    path('editor/edit_quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('editor/delete_quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),


]
