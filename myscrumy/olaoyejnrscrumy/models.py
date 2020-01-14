from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GoalStatus(models.Model):
    status_name = models.CharField(max_length=300)


class ScrumyGoals(models.Model):
    goal_name = models.CharField(max_length=200)
    goal_id = models.IntegerField()
    created_by = models.CharField(max_length=300)
    moved_by = models.CharField(max_length=300)
    owner = models.CharField(max_length=100)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='users')


class ScrumyHistory(models.Model):
    moved_by = models.CharField(max_length=200)
    created_by = models.CharField(max_length=300)
    moved_from = models.CharField(max_length=200)
    moved_to = models.CharField(max_length=200)
    time_of_action = models.TimeField()
    goal = models.ForeignKey(ScrumyGoals, on_delete=models.PROTECT)
