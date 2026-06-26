# post (second app)

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from account.models import Profile

class Post(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image=models.ImageField(
        upload_to="posts/",
        null=True,
        blank=True
    )
    saved_by=models.ManyToManyField(
        Profile,
        related_name='saved_posts',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title