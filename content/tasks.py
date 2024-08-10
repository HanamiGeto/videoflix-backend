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
        target = source[0:len(source) - 4] + '{}.m3u8'.format(key)
        cmd = ('ffmpeg -i "{}" -vf "scale={}" -start_number 0 -hls_time 5 -hls_list_size 0 -f hls "{}"').format(source, value, target)
        subprocess.run(cmd)
        
def create_thumbnails(video_instance):
    source = video_instance.video_file.path
    file_name, _ = os.path.splitext(source)
    base_name = os.path.basename(file_name)
    video_1080p_source = '{}_1080p.m3u8'.format(file_name)
    target = '{}.jpg'.format(base_name)
    thumbnail_folder = os.path.join(settings.MEDIA_ROOT, 'thumbnails')

    if not os.path.exists(thumbnail_folder):
        os.makedirs(thumbnail_folder)

    media_path = os.path.join(thumbnail_folder, target)

    result = subprocess.run(
        ['ffmpeg', '-i', video_1080p_source, '-hide_banner'],
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    duration_line = [x for x in result.stderr.split('\n') if 'Duration' in x]
    duration = duration_line[0].split(',')[0].split()[1]
    
    # Convert duration to seconds
    h, m, s = duration.split(':')
    total_seconds = int(h) * 3600 + int(m) * 60 + float(s)

    # Calculate the midpoint
    midpoint = total_seconds / 2

    cmd = 'ffmpeg -ss {} -i "{}" -vf "scale=iw:ih:force_original_aspect_ratio=decrease" -vframes 1 -update 1 "{}"'.format(midpoint, video_1080p_source, media_path)
    subprocess.run(cmd)

    video_instance.thumbnail_file = os.path.join('thumbnails', target)
    video_instance.save()