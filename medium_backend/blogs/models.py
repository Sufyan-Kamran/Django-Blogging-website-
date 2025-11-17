from django.conf import settings
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    """Tags like 'Django', 'Python', 'React'"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Main blog post model"""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, default="Blog", null=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    views = models.IntegerField(max_length=11, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comments on posts"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("author", "post_id")
