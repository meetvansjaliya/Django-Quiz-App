from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="QuizHome"),
    path('quizview/<int:myid>', views.quizView, name="Quiz List"),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('result/<int:user_id>', views.result, name='result'),
    path('saveans/', views.saveans, name='saveans'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
]