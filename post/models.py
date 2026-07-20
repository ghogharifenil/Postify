from django.db import models
from account.models import Profile

# --------------------------------------------------------------------------------
# -------------------------+ POST MODEL +-----------------------------------------
# --------------------------------------------------------------------------------


class Post(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(
        upload_to="posts/",
        null=True,
        blank=True
    )
    saved_by = models.ManyToManyField(
        Profile,
        related_name='saved_posts',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def is_liked_by(self, profile):
        return self.likes.filter(user=profile).exists()

    @property
    def first_image(self):
        image = self.images.first()

        if image:
            return image.image.url

        if self.image:
            return self.image.url

        return None


    @property
    def total_images(self):
        return self.images.count()

# -------------------------+ MULTIPLE IMAGES UPLODE MODEL +----------------------


class PostImage(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='post_images/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.post.id} - Image {self.id}"


# --------------------------------------------------------------------------------
# -------------------------+ NOTIFICATION MODEL +---------------------------------
# --------------------------------------------------------------------------------


class Notification(models.Model):

    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    receiver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="received_notifications"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    notification_type = models.CharField(max_length=20)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


# --------------------------------------------------------------------------------
# -------------------------+ LIKE MODEL +-----------------------------------------
# --------------------------------------------------------------------------------

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.user.username} liked {self.post.id}"
