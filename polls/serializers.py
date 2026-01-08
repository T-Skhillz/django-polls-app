from polls.models import Question, Choice, Vote
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class QuestionMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "url"]

class ChoiceMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "choice_text"]

class ChoiceSerializer(serializers.ModelSerializer): 
    question = QuestionMinimalSerializer(read_only=True)
    class Meta:
        model = Choice
        fields = ["id", "choice_text", "choice_votes", "question"] 

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True) #from related_name
    user = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Question
        fields = ["id", "user", "url", "title", "completed", "choices"]

class VoteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["choice"]

    def validate(self, attrs):
        user = self.context["request"].user
        choice = attrs["choice"]
        question = choice.question

        instance = Vote(
            user=user,
            choice=choice,
            question=question,
            id=self.instance.id if self.instance else None
        )
        try:
            instance.clean()
        except ValidationError as e:
        # This turns the "Crash" into a "Friendly Message"
            raise serializers.ValidationError({"choice": e.message})

        return attrs

class VoteReadSerializer(serializers.ModelSerializer):
    question_details = QuestionMinimalSerializer(source="question", read_only=True)
    choice_details = ChoiceMinimalSerializer(source="choice", read_only=True)
    user_name = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Vote
        fields = ["id", "choice_details", "question_details", "user_name", "created_at"]
