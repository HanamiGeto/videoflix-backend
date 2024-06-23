from datetime import date
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

    def __str__(self):
        return self.title
