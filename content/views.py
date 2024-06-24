from rest_framework.views import APIView
from .serializers import VideoSerializer
from .models import Video
from rest_framework.response import Response
from rest_framework import status

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