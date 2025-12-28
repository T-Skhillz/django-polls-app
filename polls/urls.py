from polls import views 
from django.urls import path, include

urlpatterns = [
    path("", views.api_root, name = "api_root"),
    path("questions/", views.QuestionList.as_view(), name = "question_list"),
    path("questions/<int:pk>/", views.QuestionDetail.as_view(), name = "question_detail"),
    path('choices/<int:pk>/vote/', views.choice_vote, name = "vote"),
    path('users/', views.UserList.as_view(), name = "user_list"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name = "user_detail"),
]