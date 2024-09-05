from rest_framework.views import APIView
from .serializers import VideoSerializer
from .models import UserVideoList, Video
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoList(APIView):
    @method_decorator(cache_page(CACHE_TTL))

    def get(self, request):
        videos = Video.objects.all().order_by('id')
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VideoDetail(APIView):
    @method_decorator(cache_page(CACHE_TTL))

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = VideoSerializer(video, context={'request': request})
        return Response(serializer.data)
    
class UserVideoListView(APIView):

    def get(self, request):
        user_videos = UserVideoList.objects.filter(user=request.user).order_by('-added_at')
        videos = [user_video.video for user_video in user_videos]
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request):
        video_id = request.data.get('id')
        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

        user_video = UserVideoList.objects.filter(user=request.user, video=video).first()

        if user_video:
            user_video.delete()
            return Response({'status': 'Video removed from list.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            UserVideoList.objects.create(user=request.user, video=video)
            return Response({'status': 'Video added to list.'}, status=status.HTTP_201_CREATED)
