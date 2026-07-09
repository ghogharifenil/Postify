# account (first app)
from django.db import models


class Profile(models.Model):

    name = models.CharField(max_length=100,  default="")

    username = models.CharField(
        max_length=50,
        unique=True,
        default=""
    )
    city = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    public_profile = models.BooleanField(
        default=True
    )

    show_city = models.BooleanField(
        default=True
    )

    profile_pic = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True
    )


def __str__(self):
    return self.username
