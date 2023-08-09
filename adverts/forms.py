from django.forms import ModelForm
from .models import Advert


class NewAdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = ["category", "header", "text"]
