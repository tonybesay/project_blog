from django.contrib import admin
from .models import ArticleReviewModel


# Register your models here.
@admin.register(ArticleReviewModel)
class ArticleReviewAdmin(admin.ModelAdmin):
    list_display = ('article', 'reviewer', 'comment', 'created_at')
    list_filter = ('article', 'created_at')