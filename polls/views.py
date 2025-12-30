from polls.models import Question, Choice, Vote
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from polls.serializers import QuestionSerializer, ChoiceSerializer, UserSerializer
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from polls.services.permissions import IsOwnerOrAuthenticated
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

# class QuestionList(APIView):
#     def get_object_list(self):
#         return Question.objects.all()

#     def get(self, request, format=None):
#         questions = self.get_object_list()
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         questions = self.get_object_list()
#         serializer = QuestionSerializer(questions, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def perform_create(self, serializers):
#         return serializers.save(user=self.request.user)
    
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

# class QuestionDetail(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Question, pk=pk)

#     def get(self, request, pk, format=None):
#         question = self.get_object(pk)
#         serializer = QuestionSerializer(question, context = {"request":request})
#         return Response(serializer.data)

#     def patch(self, request, pk, format=None):
#         question = self.get_object(pk)
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         question = self.get_object(pk)
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "user" : reverse("user_list", request=request, format=None),
            "questions" : reverse("question_list", request=request, format=None),
        }
    )

class QuestionList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

@api_view(["POST"])
def choice_vote(request, pk):
    vote = get_object_or_404(Vote, pk=pk)
    vote.votes = F("votes") + 1 #Do the math directly on the DB not Python
    vote.save()
    vote.refresh_from_db()
    serializer = ChoiceSerializer(choice)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAuthenticated]