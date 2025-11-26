from django.urls import path
from .views import *

app_name = "article"

urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    path("create/", ArticleCreateView.as_view(), name="create"),
    path('update/<int:pk>/', ArticleUpdateView.as_view(), name='update'),
    path("confirm_delete/<int:pk>/", ArticleDeleteView.as_view(), name="delete"),
    path("public/<int:pk>", PublicArticleDetailView.as_view(), name="public"),
    path("<int:pk>/comment/delete/", ArticleDeleteCommentView.as_view(), name="comment_delete"),
    path("like/", toggle_like, name="toggle_like"),
] 