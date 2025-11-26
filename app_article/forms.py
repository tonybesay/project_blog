from django import forms
from .models import ArticleModel, ArticleCommentModel


class ArticleForm(forms.ModelForm):
    submit_for_review = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

    class Meta:
        model = ArticleModel
        fields = ['title', 'content', 'category', 'cover_image']
        

class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleCommentModel
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe un comentario...'}),
        }