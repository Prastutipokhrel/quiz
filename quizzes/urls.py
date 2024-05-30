from django.urls import path
from . import views
app_name = 'quiz'
urlpatterns = [
    # quiz views
    path('home', views.start_page, name='home'),
    path('quiz_get', views.quiz_get, name='quiz_get'),
    path('submit', views.quiz_post, name='quiz_post'),
    path('next', views.next_question, name='next_question'),

    path('reset', views.reset_quiz, name='reset_quiz'),


]
