from rest_framework import serializers
from .models import StepRecord, Workouts
from django.db.models import Sum
from django.contrib.auth.models import User

class StepRecordSerializer(serializers.ModelSerializer):
    calories_burned = serializers.ReadOnlyField(source='caloriesburned')
    class Meta:
        model = StepRecord
        fields = ['id', 'steps', 'weight', 'date','calories_burned'] 
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source="profile.avatar")
    class Meta:
        model = User
        fields = ['username', 'email','avatar']
class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workouts
        fields = "__all__"
        read_only_fiields = ["user"]
        