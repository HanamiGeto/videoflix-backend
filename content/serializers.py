from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    video_file_resolutions = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_video_file_resolutions(self, obj):
        resolutions = ['1080p', '720p', '360p']
        return {
            res: f'/media/videos/{obj.title.lower()}_{res}.mp4' for res in resolutions
        }