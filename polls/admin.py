from django.contrib import admin
from polls.models import Question, Choice

class ChoiceAdmin(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ("title", "completed", "published_at")
    list_filter = ["completed", "published_at"]
    search_fields = ["title"]
    inlines = [ChoiceAdmin]

admin.site.register(Question, QuestionAdmin)