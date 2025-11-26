from django.urls import path
from .views import *

app_name = "review"

urlpatterns = [
    path("", ArticleReviewListView.as_view(), name="list"),
    path("<int:pk>/", ArticleReviewDetailView.as_view(), name="detail"),
    path("<int:pk>/comment/delete/", ReviewDeleteCommentView.as_view(), name="comment_delete"),
]