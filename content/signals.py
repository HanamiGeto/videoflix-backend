from .tasks import convert_videos_to_resolutions, create_thumbnails
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import django_rq
import glob

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_videos_to_resolutions, instance.video_file.path)
        queue.enqueue(create_thumbnails, instance)

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

        # Handle HLS files
        base_name, _ = os.path.splitext(file_path)
        hls_files_pattern = f'{base_name}_*.m3u8'
        ts_files_pattern = f'{base_name}_*.ts'

        # Delete the .m3u8 files
        for hls_file in glob.glob(hls_files_pattern):
            if os.path.isfile(hls_file):
                os.remove(hls_file)

        # Delete the .ts files
        for ts_file in glob.glob(ts_files_pattern):
            if os.path.isfile(ts_file):
                os.remove(ts_file)

    # Remove the thumbnail if it exists
    if instance.thumbnail_file:
        thumbnail_path = instance.thumbnail_file.path
        if os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)
