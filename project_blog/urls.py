from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("", include("app_core.urls", namespace="core")),
    path("article/", include("app_article.urls", namespace="article")),
    path("review/", include("app_review.urls", namespace="review")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
