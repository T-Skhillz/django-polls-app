from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question")
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
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="poll_choices")
    choice_text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.choice_text}"

    class Meta:
        verbose_name_plural = "Choices"
    