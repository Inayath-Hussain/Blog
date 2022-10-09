from django.forms import ModelForm
from .models import BlogPost


class CreateForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'blog']
