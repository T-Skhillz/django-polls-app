from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Seeds the database with sample questions, choices, and votes"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # 1. Create a Sample User if none exists
        user, _ = User.objects.get_or_create(username="tester", is_staff=True)
        user.set_password("password123")
        user.save()

        # 2. Sample Data
        data = {
            "What is your favorite Python framework?": ["Django", "Flask", "FastAPI", "Pyramid"],
            "Which database do you prefer?": ["PostgreSQL", "MySQL", "SQLite", "MongoDB"],
            "Best IDE for Python?": ["VS Code", "PyCharm", "Sublime Text", "Vim"],
        }

        for q_text, choices in data.items():
            # Create Question
            question, created = Question.objects.get_or_create(
                title=q_text, 
                user=user,
                defaults={'published_at': timezone.now()}
            )

            if created:
                # Create Choices
                for c_text in choices:
                    Choice.objects.create(question=question, choice_text=c_text)
                
                self.stdout.write(self.style.SUCCESS(f"Created Question: {q_text}"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database!"))  