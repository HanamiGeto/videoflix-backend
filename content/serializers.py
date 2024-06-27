from rest_framework import serializers
from .models import Video
import os

class VideoSerializer(serializers.ModelSerializer):
    video_file_resolutions = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_video_file_resolutions(self, obj):
        resolutions = ['_1080p', '_720p', '_360p']
        file_path, ext = os.path.splitext(str(obj.video_file))
        return {
            res: f'/media/{file_path}{res}{ext}' for res in resolutions
        }