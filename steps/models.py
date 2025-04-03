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
        return round(self.steps * self.weight * 0.03,2)
    
class Workouts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Workout_name = models.TextField(blank=False)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
