import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from steps.models import StepRecord  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Generate test data for StepRecord'

    def handle(self, *args, **kwargs):
        # Get the user you want to generate data for (you can modify this as needed)
        user = User.objects.get(username="taiwo1")  # Change this to get the specific user

        if not user:
            self.stdout.write(self.style.ERROR("No users found"))
            return

        Records = StepRecord.objects.filter(user=user)
        for record in Records:
            self.stdout.write(self.style.SUCCESS(f"steps:{record.steps} date:{record.date}"))