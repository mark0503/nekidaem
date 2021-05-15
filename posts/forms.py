from django import forms
from django.utils.translation import gettext_lazy
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'description')
        labels = {
            'text': gettext_lazy('text'),
            'description': gettext_lazy('description'),
        }