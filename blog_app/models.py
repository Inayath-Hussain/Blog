from django.db import models
from django.conf import settings

# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    blog = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    # edited_at = models.DateField(auto_now=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='blog')
    # image

    class Meta:
        ordering = ['-created_at']


class Comments(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()
    blog = models.ForeignKey(BlogPost,
                             on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_at']
