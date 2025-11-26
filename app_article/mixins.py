from django.contrib import messages
from django.shortcuts import redirect
from app_article.models import ArticleModel


class AuthorPermissionMixin:
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        # Si el usuario es admin o superuser → acceso total
        if request.user.is_superuser or request.user.groups.filter(name="Administrador").exists():
            return super().dispatch(request, *args, **kwargs)
        
        # Si es el autor → acceso permitido
        if obj.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        
        # Si no tiene permiso → redirigir y mostrar mensaje
        messages.error(request, "No tienes permiso para acceder a este artículo.")
        return redirect('article:list')


class ArticleStatusMixin:
    """
    Mixin para gestionar los cambios de estado de los artículos
    y mostrar mensajes contextuales con Bootstrap (success, warning, error, info).
    """
    
    STATUS_CONFIG = {
        "approve": {
            "status": ArticleModel.STATUS_APPROVED,
            "message": "✅ El artículo ha sido aprobado.",
            "level": messages.success,
            "default_comment": "Artículo aprobado por el revisor."
        },
        "reject": {
            "status": ArticleModel.STATUS_REJECTED,
            "message": "❌ El artículo ha sido rechazado.",
            "level": messages.error,
            "default_comment": "El artículo fue rechazado."
        },
        "draft": {
            "status": ArticleModel.STATUS_DRAFT,
            "message": "📝 El artículo ha sido devuelto a borradores.",
            "level": messages.warning,
            "default_comment": "Devuelto a borradores para revisión."
        },
        "pending": {
            "status": ArticleModel.STATUS_PENDING,
            "message": "⌛ El artículo se ha enviado a revisión.",
            "level": messages.info,
            "default_comment": "Pendiente de revisión."
        },
        "published": {
            "status": ArticleModel.STATUS_PUBLISHED,
            "message": "🚀 El artículo ha sido publicado.",
            "level": messages.success,
            "default_comment": "El artículo ha sido publicado."
        },

    }

    def handle_article_status(self, request, article=None, review=None):
        action = request.POST.get("action")

        # Si la acción es "comment", no cambia estado, solo devuelve éxito
        if action == "comment":
            messages.success(request, "💬 Comentario añadido correctamente.")
            return redirect(request.path)
        
        # Si la vista no pasa el artículo explícitamente, lo obtenemos del contexto
        if not article and hasattr(self, "get_object"):
            article = self.get_object()

        if not article:
            messages.error(request, "No se encontró el artículo.")
            return redirect("article:list")

        config = self.STATUS_CONFIG.get(action)
        if not config:
            messages.warning(request, "⚠️ Acción no reconocida.")
            return redirect(request.path)

        # Actualiza el estado
        article.status = config["status"]
        article.save()

        # Añade mensaje al usuario
        config["level"](request, config["message"])

        # Si hay revisión asociada y no hay comentario, añade uno por defecto
        if review:
            if not review.comment:
                review.comment = config["default_comment"]
            review.save()

        return redirect(request.path)