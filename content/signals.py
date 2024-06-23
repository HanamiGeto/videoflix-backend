from .tasks import convert_videos_to_resolutions
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_videos_to_resolutions, instance.video_file.path)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    Also deletes all resolution versions of the video.
    """
    if instance.video_file:
        file_path = instance.video_file.path
        if os.path.isfile(file_path):
            os.remove(file_path)

        resolutions = ['_1080p', '_720p', '_360p']

        base_name, extension = os.path.splitext(file_path)

        for resolution in resolutions:
            resolution_file_path = f'{base_name}{resolution}{extension}'
            if os.path.isfile(resolution_file_path):
                os.remove(resolution_file_path)
