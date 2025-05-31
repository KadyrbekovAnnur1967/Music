from django.db import models
from user.models import CustomUser

class Genre(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.genre
    
class Song(models.Model):
    name = models.CharField(max_length=50)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name