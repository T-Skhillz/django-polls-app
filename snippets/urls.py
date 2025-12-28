from snippets import views
from django.urls import path, include

urlpatterns = [
    path("snippets/", views.snippet_list, name = "snippet_list"),
    path("snippets/<int:pk>/", views.snippet_detail, name = "snippet_detail"),
]