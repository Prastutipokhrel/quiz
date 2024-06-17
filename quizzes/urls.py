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
    path('subcategory_view', views.editor_view, name='editor_view'),
    path('quiz_get', views.quiz_get, name='quiz_get'),
    path('submit', views.quiz_post, name='quiz_post'),
    path('next', views.next_question, name='next_question'),
    path('reset', views.reset_quiz, name='reset_quiz'),



    path('editor/', views.editor_view, name='editor_view'),
    path('category/', views.manage_category, name='manage_category'),
    path('category/<int:category_id>/', views.manage_category, name='manage_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),

    path('category/<int:category_id>/subcategories/', views.subcategory_view, name='subcategory_view'),
    path('category/<int:category_id>', views.manage_subcategory, name='manage_subcategory'),
    path('subcategory/<int:subcategory_id>/delete/', views.delete_subcategory, name='delete_subcategory'),

    path('subcategory/<int:subcategory_id>/problem/', views.manage_problem, name='manage_problem'),
    #this is test for editor view 
    path('subcategory/<int:subcategory_id>/addproblem/', views.add_problem, name='add_problem'),

    path('subcategory/<int:subcategory_id>/', views.subcategory_detail, name='subcategory_detail'),

    path('student/<int:category_id>/sub_category', views.student_subcategory, name='student_subcategory'),
    path('student/sub_category/<int:subcategory_id>', views.student_problem, name='student_problem'),



    # path('subcategory/<int:subcategory_id>/problem/<int:problem_id>/', views.manage_problem, name='manage_problem'),
    path('problem/<int:problem_id>/delete/', views.delete_problem, name='delete_problem'),

]
