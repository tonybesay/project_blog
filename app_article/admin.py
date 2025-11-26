from django.contrib import admin
from .models import ArticleModel
from django.utils import timezone

# Register your models here.
@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status')
    list_filter = ('status', 'author')
    search_fields = ('title', 'content', 'author__username')
    actions = ['make_published', 'send_to_pending']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status=ArticleModel.STATUS_PUBLISHED, published_at=timezone.now())
        self.message_user(request, f"{updated} artículo(s) marcados como publicados.")
    make_published.short_description = "Marcar como publicado"
    
    def send_to_pending(self, request, queryset):
        updated = queryset.update(status=ArticleModel.STATUS_PENDING)
        self.message_user(request, f"{updated} artículo(s) enviados a revisión.")
    send_to_pending.short_description = "Enviar a revisión"
    
