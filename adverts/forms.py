from django import forms
from django.forms import ModelForm
from .models import Advert, Reply

from ckeditor.widgets import CKEditorWidget


class NewAdvertForm(ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Advert
        fields = ["category", "header", "text"]


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ["text"]
