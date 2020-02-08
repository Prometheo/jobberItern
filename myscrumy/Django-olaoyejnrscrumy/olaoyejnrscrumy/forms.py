from django.contrib.auth.models import User
from django import forms
from .models import ScrumyGoals, GoalStatus
class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget= forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email','username','password']


class CreateGoalForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'user', 'goal_status']


class DevCreateGoalForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'user', 'goal_status']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['goal_status'].queryset = GoalStatus.objects.filter(status_name='Weekly Goal')
        self.fields['user'].queryset = User.objects.filter(username = user.username)

class MoveGoalForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']

class DevMoveGoalForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['goal_status'].queryset = GoalStatus.objects.exclude(status_name='Done Goal')

class QAMoveGoalForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['goal_status'].queryset = GoalStatus.objects.filter(status_name='Done Goal')