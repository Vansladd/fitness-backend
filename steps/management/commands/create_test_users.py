import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.contrib.auth.models import User
from steps.models import StepRecord

class Command(BaseCommand):
    help = "Populate the database with test users and step records"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating test users and step records...")

        # Create test users
        users = []
        for i in range(20):
            username = f"user{i+10}"
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password("password123")  # Set a default password
                user.save()
            users.append(user)

        # Generate test step records for the last 30 days
        for user in users:
            for days_ago in range(30):
                date = now().date() - timedelta(days=days_ago)
                steps = random.randint(1000, 20000)  # Random steps between 1k and 20k
                weight = random.uniform(60, 100)  # Random weight between 60kg and 100kg

                # Ensure only one record per user per day
                StepRecord.objects.update_or_create(
                    user=user,
                    date=date,
                    defaults={"steps": steps, "weight": weight},
                )

        self.stdout.write(self.style.SUCCESS("Test data populated successfully!"))
