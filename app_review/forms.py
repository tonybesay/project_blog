from django import forms
from .models import ArticleReviewModel

class ArticleReviewForm(forms.ModelForm):
    class Meta:
        model = ArticleReviewModel
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }