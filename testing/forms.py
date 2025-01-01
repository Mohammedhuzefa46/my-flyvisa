# forms.py
from django import forms
from .models import EmailSubscription

class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
        }
