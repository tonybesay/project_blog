from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ArticleModel(models.Model):
    # Status Choice
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_PUBLISHED = 'published'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICE = (
        (STATUS_DRAFT, 'Borrador'),
        (STATUS_PENDING, 'En revisión'),
        (STATUS_PUBLISHED, 'Publicado'),
        (STATUS_APPROVED, 'Aprobado'),
        (STATUS_REJECTED, 'Rechazado'),
    )
    
    author = models.ForeignKey(User, verbose_name='Autor', on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(verbose_name='Título', max_length=100)
    content = models.TextField(verbose_name='Contenido', blank=True)
    category = models.CharField(verbose_name="Categoría", max_length=50, blank=True, null=True)
    cover_image = models.ImageField(upload_to='articles/covers/', null=True, blank=True, verbose_name='Imagen de portada')
    status = models.CharField(verbose_name='Estado', choices=STATUS_CHOICE, default=STATUS_DRAFT)
    created_at = models.DateTimeField(verbose_name='Creado el', auto_now_add=True,)
    updated_at = models.DateTimeField(verbose_name='Acualizado el',auto_now=True)
    published_at = models.DateTimeField(verbose_name='Publicado el', null=True, blank=True)
    likes = models.ManyToManyField(User, verbose_name='Me gusta', related_name="liked_articles", blank=True)
    
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        verbose_name = "Artículos"
        verbose_name_plural = "Artículo"
        ordering = ['-published_at', '-created_at']
        
    def __str__(self):
        return f'{self.title} ({self.status})'
    
    
class ArticleCommentModel(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE, related_name="public_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_comments")
    comment = models.TextField(verbose_name="Comentario", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comentario público"
        verbose_name_plural = "Comentarios públicos"
        ordering = ['-created_at']

    def __str__(self):
        return f'Comentario de {self.user.username} en {self.article.title}'

