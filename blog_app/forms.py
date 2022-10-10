from django.forms import ModelForm
from .models import BlogPost, Comments


class CreateForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'blog']


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
