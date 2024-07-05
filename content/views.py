import os
from rest_framework.views import APIView
from .serializers import VideoSerializer
from .models import Video
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# @login_required
@cache_page(CACHE_TTL)
def protected_media(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, 'videos', path)
    if os.path.exists(media_path):
        return FileResponse(open(media_path, 'rb'))
    else:
        return HttpResponseForbidden('Forbidden')

class VideoList(APIView):
    authentication_classes = []
    permission_classes = []
    @method_decorator(cache_page(CACHE_TTL))

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VideoDetail(APIView):
    authentication_classes = []
    permission_classes = []
    @method_decorator(cache_page(CACHE_TTL))

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = VideoSerializer(video)
        return Response(serializer.data)