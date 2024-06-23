import subprocess

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
        