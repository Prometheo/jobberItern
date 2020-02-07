from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from .models import ScrumyGoals,ScrumyHistory,GoalStatus
from random import randint
from .forms import SignupForm, CreateGoalForm, MoveGoalForm, DevMoveGoalForm, QAMoveGoalForm, DevCreateGoalForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def get_grading_parameters(request):
    new_message = ScrumyGoals.objects.filter(goal_name="Learn Django")[0].goal_name
    return HttpResponse(new_message)

@login_required
def move_goal(request, goal_id):
    
    # except Exception as e:
    #     return render(request, 'olaoyejnrscrumy/exception.html', {'error': 'A record with that goal id does not exist'})
    #return HttpResponse(target.goal_name)
    current_user = request.user
    user_group = current_user.groups.all()[0].name
    Dev = Group.objects.get(name = 'Developer').name
    QA = Group.objects.get(name = 'Quality Assurance').name
    Admin = Group.objects.get(name = 'Admin').name
    Owner = Group.objects.get(name = 'Owner').name

    scrumy_goals = get_object_or_404(ScrumyGoals, goal_id=goal_id)

    if user_group == Admin or user_group == Owner:
        if request.method == 'POST':
            form = MoveGoalForm(request.POST)
            if form.is_valid():
                #scrumygoals = form.save(commit=False)
                scrumy_goals.goal_status = form.cleaned_data['goal_status']
                #cur_goal = ScrumyGoals.objects.get(goal_id = goal_id)
                #cur_goal.goal_status = form.cleaned_data['status_name']
                #scrumygoals.goal_id = gen_num()
                scrumy_goals.save()
                return redirect('/olaoyejnrscrumy/home')
        else:
            form = MoveGoalForm()
            args = {'form':form, 'current_user':current_user}
            return render(request, 'olaoyejnrscrumy/movegoal.html', args)  
    elif user_group == Dev and current_user == scrumy_goals.user:
        if request.method == 'POST':
            form = DevMoveGoalForm(request.POST)
            if form.is_valid():
                scrumy_goals.goal_status = form.cleaned_data['goal_status']
                scrumy_goals.save()
                return redirect('/olaoyejnrscrumy/home')
        else:
            form = DevMoveGoalForm()
            args = {'form':form, 'current_user':current_user}
            return render(request, 'olaoyejnrscrumy/movegoal.html', args)
    elif user_group == Dev and current_user != scrumy_goals.user:
        return render(request, 'olaoyejnrscrumy/denied.html')
        #return render(request, 'olaoyejnrscrumy/movegoal.html')

    elif user_group == QA and scrumy_goals.goal_status.status_name == 'Verify Goal':
        if request.method == 'POST':
            form = QAMoveGoalForm(request.POST)
            if form.is_valid():
                scrumy_goals.goal_status = form.cleaned_data['goal_status']
                scrumy_goals.save()
                return redirect('/olaoyejnrscrumy/home')
        else:
            form = QAMoveGoalForm()
            args = {'form':form, 'current_user':current_user}
            return render(request, 'olaoyejnrscrumy/movegoal.html', args)

    elif user_group == QA and current_user == scrumy_goals.user:
        if request.method == 'POST':
            form = MoveGoalForm(request.POST)
            if form.is_valid():
                scrumy_goals.goal_status = form.cleaned_data['goal_status']
                scrumy_goals.save()
                return redirect('/olaoyejnrscrumy/home')
        
        else:
            form = MoveGoalForm()
            args = {'form':form, 'current_user':current_user}
            return render(request, 'olaoyejnrscrumy/movegoal.html', args)


    elif user_group == QA and scrumy_goals.goal_status.status_name != 'Verify Goal':
        return render(request, 'olaoyejnrscrumy/QAdenied.html')



def gen_num():
    not_unique = True
    while not_unique:
        num = randint(1000,9999)
        not_unique = ScrumyGoals.objects.filter(goal_id=num).exists()
    return num


@login_required
def  add_goal(request):
    current_user = request.user
    user_group = current_user.groups.all()[0].name
    Dev = Group.objects.get(name = 'Developer').name
    QA = Group.objects.get(name = 'Quality Assurance').name
    Admin = Group.objects.get(name = 'Admin').name
    Owner = Group.objects.get(name = 'Owner').name
    if user_group == Dev or QA:
        if request.method == 'POST':
            form = DevCreateGoalForm(request.user, request.POST)
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
            form = DevCreateGoalForm(request.user)
            args = {'form':form}
            return render(request, 'olaoyejnrscrumy/addgoal.html', args)
    return render(request, 'olaoyejnrscrumy/addgoal.html')
@login_required
def home(request):
    # record_list = ScrumyGoals.objects.get(goal_name = 'Learn Django')
    # context = {'goal_name': record_list.goal_name, 'goal_id': record_list.goal_id, 'user': record_list.user}
    
    All_Users = User.objects.all()
    wikly_goals = GoalStatus.objects.filter(status_name = "Weekly Goal")
    All_weekly_goals = [goals.scrumygoals_set.all() for goals in wikly_goals][0]
    #All_weekly_goals = wikly_goals.scrumygoals_set.all()

    daily_goals = GoalStatus.objects.filter(status_name = "Daily Goal")
    All_daily_goals =  [goals.scrumygoals_set.all() for goals in daily_goals][0]

    veri_goals = GoalStatus.objects.filter(status_name = "Verify Goal")
    All_veri_goals = [goals.scrumygoals_set.all() for goals in veri_goals][0]

    done_goals = GoalStatus.objects.filter(status_name = "Done Goal")
    All_done_goals = [goals.scrumygoals_set.all() for goals in done_goals][0]

    user = request.user
    rank = user.groups.all()[0].name

    Contexts = {'rank': rank, 'All_Users': All_Users, 'All_weekly_goals': All_weekly_goals, "All_daily_goals": All_daily_goals, "All_veri_goals": All_veri_goals, "All_done_goals": All_done_goals}

    return render(request, 'olaoyejnrscrumy/home.html', Contexts)

def success_page(request):
    return render(request, 'olaoyejnrscrumy/message.html')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password']
            )
            new_user.save()
            dev_group = Group.objects.get(name='Developer')
            dev_group.user_set.add(new_user)
            return redirect('/olaoyejnrscrumy/success_message')
    else:
        form = SignupForm()

        args = {'form':form}
        return render(request, 'registration/index.html', args)