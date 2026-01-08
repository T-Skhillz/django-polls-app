from polls.models import Question, Choice, Vote
from polls.serializers import (
    QuestionSerializer,
    ChoiceSerializer,
    VoteReadSerializer,
    VoteWriteSerializer,
)

from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from polls.services.permissions import IsOwnerOrAuthenticated


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        question = self.get_object()
        # Get all choices for this question and count their votes
        choices = question.choices.annotate(_vote_count=Count('choice_votes'))
        
        results_data = [
            {
                "id": choice.id,
                "text": choice.choice_text,
                "votes": choice._vote_count
            }
            for choice in choices
        ]
        
        return Response({
            "question": question.title,
            "results": results_data
        })

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return VoteReadSerializer
        return VoteWriteSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Vote.objects.none()
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)