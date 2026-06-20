# account (first app)
from django.db import models

class Profile(models.Model):

    name = models.CharField(max_length=100,  default="")

    username = models.CharField(
        max_length=50,
        unique=True,
        default=""
    )

    email = models.EmailField()

    bio = models.TextField(blank=True)

    profile_pic = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
    