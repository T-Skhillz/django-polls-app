from django.contrib import admin
from snippets.models import Snippet

class SnippetAdmin(admin.ModelAdmin):
    list_display = ("title", "language","style" , "linenos", "created_at")
    list_filter = ["language", "style", "created_at"]
    search_fields = ["language", "title", "created_at"]

admin.site.register(Snippet, SnippetAdmin)