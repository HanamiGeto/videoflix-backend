from django.urls import path
from .views import UserVideoListView, VideoDetail, VideoList

urlpatterns = [
    path('videos/', VideoList.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetail.as_view(), name='video-detail'),
    path('my-videos/', UserVideoListView.as_view(), name='user-video-list')
]