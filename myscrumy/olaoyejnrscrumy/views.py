from django.shortcuts import render
from django.http import HttpResponse
from .models import ScrumyGoals,ScrumyHistory,GoalStatus

# Create your views here.
new_message = ScrumyGoals.objects.filter(goal_name="Learn Django")[0].goal_name

def get_grading_parameters(request):
    return HttpResponse(new_message)