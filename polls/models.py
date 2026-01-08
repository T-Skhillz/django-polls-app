from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=200)
    published_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["-published_at"]
        verbose_name_plural = "Questions"
        verbose_name = "Question"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=300)

    def votes_count(self):
        return self.choice_votes.count()

    def __str__(self):
        return f"{self.choice_text}"

    class Meta:
        verbose_name_plural = "Choices"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_votes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_votes", blank=True, editable=False)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="choice_votes")
    created_at = models.DateTimeField(default=timezone.now)    

    def clean(self):
        if self.choice_id and self.user_id:
            exist = Vote.objects.filter(
                user=self.user,
                question=self.choice.question
            ).exclude(id=self.id).exists()

            if exist:
                raise ValidationError("This user has already voted in this poll.")

    def save(self, *args, **kwargs):
        # Automatically link the vote to the question via the choice
        if not self.question_id and self.choice_id:
            self.question = self.choice.question
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} voted '{self.choice}' on question '{self.question}'"
    
    class Meta:
        verbose_name_plural = "Votes"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "question"],
                name="unique_user_question_vote"
            )
        ]
        indexes = [
            models.Index(fields=["question", "choice"]) #useful for counting votes
        ]
    