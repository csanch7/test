from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")

    def serialize(self):
        return {
            "followers": self.followers,
            "following": self.following,
        }




class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    postcontent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likecount = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "postcontent": self.postcontent,
            "timestamp": self.timestamp,
            "likecount": self.likecount
        }
    def __str__(self):
        return f"{self.postcontent}"
    

