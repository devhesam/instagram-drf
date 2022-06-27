from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    STATUS_CHOICES=[
        ('accept','Accept'),
        ('pending','Pending')
    ] 
    user=models.CharField(max_length=30)
    followers=models.ForeignKey(User,related_name='followers',null=True,blank=True,on_delete=models.CASCADE)
    following=models.ForeignKey(User,related_name='followings',null=True,blank=True,on_delete=models.CASCADE)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')

    def __str__(self) -> str:
        return self.user
