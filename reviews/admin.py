from django.contrib import admin
from .models import ReviewReport


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('filename', 'created_at')
    readonly_fields = ('created_at',)
