from polls import views 
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r"questions", views.QuestionViewSet, basename="question")
router.register(r"choices", views.ChoiceViewSet, basename="choice")
router.register(r"votes", views.VoteViewSet, basename="vote")

urlpatterns = [
    path("api/v1/", include(router.urls)),

    #path("", views.api_root, name = "api_root"),
    #path("questions/", views.QuestionList.as_view(), name = "question_list"),
    #path("questions/<int:pk>/", views.QuestionDetail.as_view(), name = "question_detail"),
    #path("questions/<int:pk>/choices/", views.ChoiceList.as_view(), name = "choice_list"),
    #path('users/', views.UserList.as_view(), name = "user_list"),
    #path('users/<int:pk>/', views.UserDetail.as_view(), name = "user_detail"),
]