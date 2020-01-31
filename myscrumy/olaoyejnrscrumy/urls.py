from django.urls import path, include
from . import views
from .models import SignupForm, CreateGoalForm

urlpatterns = [
    path('', views.get_grading_parameters),
    path('movegoal/<int:goal_id>', views.move_goal, name="move_goal"),
    path('addgoal', views.add_goal),
    path('home', views.home, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register', views.register, name="registration"),
    path('addgoal', views.add_goal, name="AddGoal"),
]

app_name = 'olaoyejnrscrumy'
#app_name = 'accounts'