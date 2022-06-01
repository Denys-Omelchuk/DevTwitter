from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    body = models.CharField(max_length=250, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body


class Comment(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=250, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body
