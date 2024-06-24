from django.urls import path
from .views import VideoDetail, VideoList

urlpatterns = [
    path('videos/', VideoList.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetail.as_view(), name='video-detail'),
]