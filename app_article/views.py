from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView, FormView
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .forms import ArticleForm, ArticleCommentForm
from .mixins import ArticleStatusMixin
from app_review.forms import ArticleReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from app_user.mixins import GroupRequiredMixin
from .mixins import AuthorPermissionMixin
from django.contrib.messages.views import SuccessMessageMixin



class ArticleListView(LoginRequiredMixin, GroupRequiredMixin, ArticleStatusMixin, ListView):
    model = ArticleModel
    template_name = 'article/article_list.html'
    context_object_name = 'articles'
    group_required = "Autor"

    def get_queryset(self):
        queryset = ArticleModel.objects.all()
        
        # Filtro por estado
        status = self.request.GET.get('status')
        if status in ['pending', 'approved', 'rejected', 'draft', 'published']:
            queryset = queryset.filter(status=status)

        # Filtro por autor
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author__username__icontains=author)

        # Filtro por categoría
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)
            
        return queryset


class ArticleDetailView(LoginRequiredMixin, GroupRequiredMixin, ArticleStatusMixin, AuthorPermissionMixin, DetailView):
    model = ArticleModel
    form_class = ArticleReviewForm
    template_name = 'article/article_detail.html'
    context_object_name = 'article'
    group_required = "Autor"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        article = self.get_object()

        if form.is_valid():
            comment = form.cleaned_data.get("comment", "").strip()
            action = self.request.POST.get("action")
            if not comment and action == "comment":
                messages.warning(self.request, "⚠️ No se puede añadir un comentario vacío.")
                return redirect("article:detail", pk=article.pk)
            
            review = form.save(commit=False)
            review.article = article
            review.reviewer = request.user
            review.save()

        return self.handle_article_status(request, article=article)
        
    
class ArticleCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = ArticleModel
    template_name = 'article/article_create.html'
    form_class = ArticleForm
    group_required = "Autor"

    
    def form_valid(self, form):
        form.instance.author = self.request.user
        action = self.request.POST.get('action')
    
        
        if action == 'submit_review':
            form.instance.status = ArticleModel.STATUS_PENDING
        elif action == "save_draft":
            form.instance.status = ArticleModel.STATUS_DRAFT
        messages.success(self.request, ("Publicación creada correctamente"))
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse_lazy('article:detail', kwargs={"pk": self.object.pk})
    
    
class ArticleUpdateView(LoginRequiredMixin, GroupRequiredMixin, AuthorPermissionMixin, UpdateView):
    model = ArticleModel
    template_name = 'article/article_update.html'
    group_required = "Autor"
    fields = ['title','content', 'category', 'cover_image']
    
    def form_valid(self, form):
        messages.success(self.request, ("Artículo actualizado correctamente"))
        action = self.request.POST.get('action')
        
        if action == 'submit_review':
            form.instance.status = ArticleModel.STATUS_PENDING
        elif action == "save_draft":
            form.instance.status = ArticleModel.STATUS_DRAFT
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('article:detail', kwargs={"pk": self.object.pk})
     
    
class ArticleDeleteView(LoginRequiredMixin, GroupRequiredMixin, AuthorPermissionMixin, SuccessMessageMixin, DeleteView):
    model = ArticleModel
    template_name = 'article/article_confirm_delete.html'
    success_url =  reverse_lazy('article:list')
    group_required = "Autor"
    success_message = "Artículo eliminado correctamente"
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

class PublicArticleDetailView(DetailView, FormView):
    model = ArticleModel
    form_class = ArticleCommentForm
    template_name = 'article/article_public_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        # Solo mostrar artículos publicados
        return ArticleModel.objects.filter(status=ArticleModel.STATUS_PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = self.form_class()
        context["comments"] = self.object.public_comments.all()
        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.cleaned_data.get("comment", "").strip()
            if not comment:
                messages.warning(request, "⚠️ No puedes enviar un comentario vacío.")
                return redirect("article:public", pk=article.pk)

            comment_obj = form.save(commit=False)
            comment_obj.article = article
            comment_obj.user = request.user
            comment_obj.save()

            messages.success(request, "💬 Comentario publicado correctamente.")
            return redirect("article:public", pk=article.pk)

        messages.error(request, "❌ Ocurrió un error al publicar el comentario.")
        return redirect("article:public", pk=article.pk)


class ArticleDeleteCommentView(DeleteView):
    model = ArticleCommentModel
    
    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        
        # Solo el autor o superusuario pueden eliminar
        if comment.user != request.user and not request.user.is_superuser:
            return JsonResponse({'error': 'No tienes permiso para eliminar este comentario.'}, status=403)

        article = comment.article
        comment.delete()
        
        # Si es una petición AJAX devolvemos JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Comentario eliminado correctamente.', 'id': comment.pk})

        # Si no, redirigimos como antes
        return redirect('article:public', pk=article.pk)


@login_required
@require_POST
def toggle_like(request):
    article_id = request.POST.get("article_id")
    article = ArticleModel.objects.get(pk=article_id)

    if request.user in article.likes.all():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": article.total_likes(),
    })
    
    