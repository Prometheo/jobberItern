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
    try:
        target = ScrumyGoals.objects.get(goal_id=goal_id)
    except Exception as e:
        return render(request, 'olaoyejnrscrumy/exception.html', {'error': 'A record with that goal id does not exist'})
    else:
        return HttpResponse(target.goal_name)


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
    # record_list = ScrumyGoals.objects.get(goal_name = 'Learn Django')
    # context = {'goal_name': record_list.goal_name, 'goal_id': record_list.goal_id, 'user': record_list.user}
    
    All_Users = User.objects.all()
    wikly_goals = GoalStatus.objects.get(status_name = "Weekly Goal")
    All_weekly_goals = wikly_goals.scrumygoals_set.all()

    daily_goals = GoalStatus.objects.get(status_name = "Daily Goal")
    All_daily_goals = daily_goals.scrumygoals_set.all()

    veri_goals = GoalStatus.objects.get(status_name = "Verify Goal")
    All_veri_goals = veri_goals.scrumygoals_set.all()

    done_goals = GoalStatus.objects.get(status_name = "Done Goal")
    All_done_goals = done_goals.scrumygoals_set.all()

    Contexts = {'All_Users': All_Users, 'All_weekly_goals': All_weekly_goals, "All_daily_goals": All_daily_goals, "All_veri_goals": All_veri_goals, "All_done_goals": All_done_goals}

    return render(request, 'olaoyejnrscrumy/home.html', Contexts)