from django.db import models
from app_article.models import ArticleModel
from django.contrib.auth.models import User


# Create your models here.
class ArticleReviewModel(models.Model):
    article = models.ForeignKey(ArticleModel, verbose_name='Artículo', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, verbose_name='Revisor', on_delete=models.SET_NULL, null=True, blank=True, related_name='article_reviews')
    comment = models.TextField(verbose_name='Comentario', blank=True)
    created_at = models.DateTimeField(verbose_name='Creado el', auto_now_add=True)
    
    class Meta:
        verbose_name = "Revisión"
        verbose_name_plural = "Revisiones"
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Review {self.pk} - {self.article.title} by {self.reviewer}'