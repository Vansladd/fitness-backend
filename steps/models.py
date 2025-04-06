from django.db import models
from django.contrib.auth.models import User
from  django.utils import timezone
# Create your models here.


class StepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField()
    weight = models.FloatField()
    date = models.DateField(default= timezone.now)

    def caloriesburned(self):
        calories = self.steps * self.weight * 0.03
        return round(calories,2)
    
class Workouts(models.Model):
    WORKOUT_TYPES = [
        ("running", "Running"),
        ("weightlifting", "Weightlifting"),
        ("cycling", "Cycling"),
        ("yoga", "Yoga"),
        ("swimming", "Swimming"),
        ("other", "Other"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    workout_type = models.CharField(max_length=30, choices=WORKOUT_TYPES, default="other")
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout_type} on {self.date}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=100, default='default-user')

    def __str__(self):
        return f"{self.user.username}'s profile"
