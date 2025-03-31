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

        base_steps = 5000  # Starting point for steps
        step_range = 2000  # Range of randomness to add to the base steps (±2000)
        num_days = 30  # Generate for 30 days

        for day_offset in range(num_days):
            date = datetime.today().date() - timedelta(days=day_offset)
            self.stdout.write(f"Date created: {date}")
            random_step_variation = random.randint(-step_range, step_range)
            daily_steps = base_steps + random_step_variation
            daily_steps = max(daily_steps, 0)  # Ensure no negative steps

            # Create a StepRecord for the user and the date
            self.stdout.write(f"Date created: {date}")
            StepRecord.objects.create(
                user=user,
                steps=daily_steps,
                weight=70.5,  # Example weight, modify this based on the user
                date=date
            )

        self.stdout.write(self.style.SUCCESS(f"Generated {num_days} test step records for user {user.username}."))
