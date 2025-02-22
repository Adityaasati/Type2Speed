from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    """Form for user feedback submission."""
    class Meta:
        model = Feedback
        fields = ['email', 'suggestion']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'suggestion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Suggestion', 'rows': 4}),
        }
