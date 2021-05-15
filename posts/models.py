from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class Post(models.Model):
    text = models.TextField('текст')
    pub_date = models.DateField('дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Посты'
    
    def __str__(self):
        return self.description[:15]

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    