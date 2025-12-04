from django.db import models


class ReviewReport(models.Model):
    filename = models.CharField(max_length=255)
    code_content = models.TextField()
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} — {self.created_at:%Y-%m-%d %H:%M}"
