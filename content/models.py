from datetime import date
from django.conf import settings
from django.db import models

class Video(models.Model):
    GENRE = (
        ('nature', 'Nature'),
        ('animals', 'Animals'),
        ('animated', 'Animated'),
    )
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    genre = models.CharField(
        max_length=10, 
        choices=GENRE
    )
    video_file = models.FileField(upload_to='videos')
    thumbnail_file = models.FileField(upload_to='thumbnails', null=True, blank=True)

    def __str__(self):
        return self.title

class UserVideoList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.title