from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField()
    weight = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def caloriesburned(self):
        return round(self.steps * self.weight * 0.03,2)
