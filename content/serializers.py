from rest_framework import serializers
from .models import Video
import os

class VideoSerializer(serializers.ModelSerializer):
    video_file_resolutions = serializers.SerializerMethodField()
    genre_display = serializers.CharField(source='get_genre_display', read_only=True)

    class Meta:
        model = Video
        fields = '__all__'

    def get_video_file_resolutions(self, obj):
        resolutions = ['_1080p', '_720p', '_360p']
        request = self.context.get('request')
        file_path, ext = os.path.splitext(str(obj.video_file).replace('\\', '/'))
        return {
            res: request.build_absolute_uri(
                f'/media/{file_path}{res}.m3u8'
            ) for res in resolutions
        }
    
    def to_representation(self, instance):
        request = self.context.get('request')
        representation = super().to_representation(instance)

        video_file_path = instance.video_file.name.replace('\\', '/')
        thumbnail_file_path = instance.thumbnail_file.name.replace('\\', '/') 

        representation['video_file'] = request.build_absolute_uri(
            f'/media/{video_file_path}'
        )
        representation['thumbnail_file'] = request.build_absolute_uri(
            f'/media/{thumbnail_file_path}'
        )
        return representation