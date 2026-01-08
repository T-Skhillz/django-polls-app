from django.contrib import admin
import nested_admin
from polls.models import Question, Choice, Vote
from django.db.models import Count

class VoteAdmin(nested_admin.NestedTabularInline):
    model = Vote
    extra = 0
    classes = ["collapse"]
    readonly_fields = ("created_at", "display_question")
    fields = ("user", "created_at")
    raw_id_fields = ("user",)
    autocomplete_fields = ("user",)
    fk_name = "choice"

    def display_question(self, obj):
        return obj.question.title if obj.question else "-"
    display_question.short_description = "Question"

class ChoiceAdmin(nested_admin.NestedTabularInline):
    model = Choice
    inlines = [VoteAdmin]
    fields = ("choice_text", "votes_count")
    readonly_fields = ("votes_count",)
    extra = 1

@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin):
    model = Question
    list_display = ("title", "user", "completed", "published_at", "display_total_votes")
    list_filter = ("completed", "published_at", "user")
    search_fields = ("title",)
    date_hierarchy = "published_at"
    inlines = [ChoiceAdmin]
    readonly_fields = ("published_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _vote_count = Count("question_votes", distinct=True)
        )
        return queryset

    def display_total_votes(self, obj):
        return obj._vote_count
    
    display_total_votes.admin_order_field = "_vote_count"
    display_total_votes.short_description = "Total Votes"