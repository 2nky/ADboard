from django.forms import ModelForm
from .models import Advert, Reply


class NewAdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = ["category", "header", "text"]


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ["text"]
