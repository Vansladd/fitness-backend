from rest_framework import serializers
from .models import StepRecord

class StepRecordSerializer(serializers.ModelSerializer):
    calories_burned = serializers.ReadOnlyField(source='caloriesburned')
    class Meta:
        model = StepRecord
        fields = ['id', 'steps', 'weight', 'date','calories_burned'] 
        read_only_fields = ['user']
        