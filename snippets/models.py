from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.db import models

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    code = models.TextField(verbose_name="code snippet")
    language = models.CharField(
        max_length=100,
        choices=LANGUAGE_CHOICES,
        default="python"
    )
    style = models.CharField(
        max_length=100,
        choices=STYLE_CHOICES,
        default="friendly"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    linenos = models.BooleanField(default=False)