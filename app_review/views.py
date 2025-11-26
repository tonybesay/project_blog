from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse

from django.views.generic import ListView, FormView, DeleteView

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


from app_article.models import ArticleModel
from .models import *
from .forms import ArticleReviewForm
from app_user.mixins import GroupRequiredMixin
from app_article.mixins import ArticleStatusMixin


class ArticleReviewListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = ArticleModel
    template_name = 'review/article_review_list.html'
    context_object_name = 'articles'
    group_required = "Revisor"
    
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

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', 'all')
        return context
    
    def post(self, request, *args, **kwargs):
        return self.process_article_action(request)
        

class ArticleReviewDetailView(LoginRequiredMixin, GroupRequiredMixin, ArticleStatusMixin, FormView):
    template_name = "review/article_review_detail.html"
    form_class = ArticleReviewForm
    group_required = "Revisor"
    context_object_name = "review"

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(ArticleModel, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = self.article
        return context

    def form_valid(self, form):

        review = form.save(commit=False)
        review.article = self.article
        review.reviewer = self.request.user
        review.save()

        action = self.request.POST.get("action")
        comment = form.cleaned_data.get("comment", "").strip()
        if not comment and action == "comment":
            messages.warning(self.request, "⚠️ No se puede añadir un comentario vacío.")
            return redirect("review:detail", pk=self.article.pk)
        
        self.handle_article_status(self.request, article=self.article, review=review)

        return redirect('review:detail', review.article.pk)
       

class ReviewDeleteCommentView(DeleteView):
    model = ArticleReviewModel
    
    def post(self, request, *args, **kwargs):
        review = self.get_object()
        
        # Solo el autor o superusuario pueden eliminar
        if review.reviewer != request.user and not request.user.is_superuser:
            return JsonResponse({'error': 'No tienes permiso para eliminar este comentario.'}, status=403)

        review.delete()
        
        # Si es una petición AJAX devolvemos JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Comentario eliminado correctamente.', 'id': review.pk})

        # Si no, redirigimos como antes
        return redirect('review:list')