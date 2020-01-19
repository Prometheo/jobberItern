from django.shortcuts import render
from django.http import HttpResponse
from .models import ScrumyGoals,ScrumyHistory,GoalStatus

# Create your views here.
def get_grading_parameters(request):
    new_message = ScrumyGoals.objects.filter(goal_name="Learn Django")[0].goal_name
    return HttpResponse(new_message)

def move_goal(request, goal_id):
    target = ScrumyGoals.objects.get(goal_id=goal_id)
    message = target.goal_name
    return HttpResponse(message)