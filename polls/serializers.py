from polls.models import Question, Choice, Vote
from rest_framework import serializers
from django.contrib.auth.models import User

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "votes"]

class ChoiceSerializer(serializers.ModelSerializer):
    choice_votes = VoteSerializer(many=True)
    class Meta:
        model = Choice
        fields = ["id", "choice_text", "choice_votes"] 
        #never include the ForeignKey back to the parent when nesting: 
        # BAD — includes the reverse FK
        #fields = ["question", "choice_text", "votes"]
        # # GOOD — exclude the reverse FK
        # fields = ["choice_text", "votes"]   # ← remove "question"

class QuestionSerializer(serializers.ModelSerializer):
    poll_choices = ChoiceSerializer(many=True, read_only=True) #from related_name
    user = serializers.ReadOnlyField(source="user.username")
    question_url = serializers.HyperlinkedIdentityField(view_name="question_detail")
    class Meta:
        model = Question
        fields = ["id", "user", "question_url", "title", "completed", "poll_choices"]

class UserSerializer(serializers.ModelSerializer):
    questions = serializers.HyperlinkedRelatedField(many = True, view_name="question_detail", read_only=True)
    #url = serializers.HyperlinkedIdentityField(view_name="question_detail")
    class Meta:
        model = User
        fields = ["id", "username", "question"]