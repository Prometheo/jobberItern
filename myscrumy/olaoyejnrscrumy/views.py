from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import ScrumyGoals,ScrumyHistory,GoalStatus
from random import randint
from .forms import SignupForm, CreateGoalForm
from django.contrib.auth.decorators import login_required
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



@login_required
def  add_goal(request):
    # user2 = User.objects.get(username='louis')
    weekGoal = GoalStatus.objects.get(status_name='Weekly Goal')
    # ScrumyGoals.objects.create(goal_name='Keep Learning Django', goal_id=gen_num(),created_by='Louis',moved_by='Louis',owner='Louis',goal_status=weekGoal,user = user2)
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        if form.is_valid():
            scrumygoals = form.save(commit=False)
            scrumygoals.user = form.cleaned_data['user']
            scrumygoals.goal_name = form.cleaned_data['goal_name']
            scrumygoals.goal_status = form.cleaned_data['goal_status']
            scrumygoals.goal_id = gen_num()

            #ScrumyGoals.objects.create(goal_name=form.cleaned_data['goal_name'], goal_id=gen_num(),goal_status= form.cleaned_data['goal_status'], user=form.cleaned_data['user'])
            scrumygoals.save()
            return redirect('/olaoyejnrscrumy/home')
    else:
        form = CreateGoalForm()

        args = {'form':form}
        return render(request, 'olaoyejnrscrumy/addgoal.html', args)
    return render(request, 'olaoyejnrscrumy/addgoal.html')
@login_required
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



def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password']
            )
            new_user.save()
            return redirect('/olaoyejnrscrumy/home')
    else:
        form = SignupForm()

        args = {'form':form}
        return render(request, 'registration/index.html', args)