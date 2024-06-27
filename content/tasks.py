import subprocess
import os
from django.conf import settings

def convert_videos_to_resolutions(source):
    resolutions = {
        '_1080p': 'hd1080',
        '_720p': 'hd720',
        '_360p': '640x360'
    }
    for key, value in resolutions.items():
        target = source[0:len(source) - 4] + '{}.mp4'.format(key)
        cmd = 'ffmpeg -i "{}" -s {} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, value, target)
        subprocess.run(cmd)
        
def create_thumbnails(video_instance):
    source = video_instance.video_file.path
    file_name, _ = os.path.splitext(source)
    base_name = os.path.basename(file_name)
    video_1080p_source = '{}_1080p.mp4'.format(file_name)
    target = '{}.jpg'.format(base_name)
    thumbnail_folder = os.path.join(settings.MEDIA_ROOT, 'thumbnails')

    if not os.path.exists(thumbnail_folder):
        os.makedirs(thumbnail_folder)

    media_path = os.path.join(thumbnail_folder, target)
    cmd = 'ffmpeg -ss 00:00:01.00 -i "{}" -vf "scale=320:320:force_original_aspect_ratio=decrease" -vframes 1 -update 1 "{}"'.format(video_1080p_source, media_path)
    subprocess.run(cmd)

    video_instance.thumbnail_file = os.path.join('thumbnails', target)
    video_instance.save()