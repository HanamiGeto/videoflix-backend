from rest_framework.views import APIView
from .serializers import VideoSerializer
from .models import Video
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os

@login_required
def protected_media(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, 'videos', path)
    if os.path.exists(media_path):
        return FileResponse(open(media_path, 'rb'))
    else:
        return HttpResponseForbidden('Forbidden')

class VideoList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
class VideoDetail(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = VideoSerializer(video)
        return Response(serializer.data)