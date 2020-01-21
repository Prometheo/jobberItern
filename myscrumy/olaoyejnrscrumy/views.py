from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import ScrumyGoals,ScrumyHistory,GoalStatus
from random import randint
# Create your views here.
def get_grading_parameters(request):
    new_message = ScrumyGoals.objects.filter(goal_name="Learn Django")[0].goal_name
    return HttpResponse(new_message)

def move_goal(request, goal_id):
    target = ScrumyGoals.objects.get(goal_id=goal_id)
    message = target.goal_name
    return HttpResponse(message)


def gen_num():
    not_unique = True
    while not_unique:
        num = randint(1000,9999)
        not_unique = ScrumyGoals.objects.filter(goal_id=num).exists()
    return num




def  add_goal(request):
    user2 = User.objects.get(username='louis')
    weekGoal = GoalStatus.objects.get(status_name='Weekly Goal')
    ScrumyGoals.objects.create(goal_name='Keep Learning Django', goal_id=gen_num(),created_by='Louis',moved_by='Louis',owner='Louis',goal_status=weekGoal,user = user2)


def home(request):
    record = ScrumyGoals.objects.filter(goal_name = 'Keep Learning Django')[0]
    return HttpResponse(record)