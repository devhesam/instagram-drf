from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username



class Comment(models.Model):
    author = models.ForeignKey(User, related_name='authors', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='posts_comments', on_delete=models.CASCADE)
    created_time = models.DateField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.pk}---{self.author}'