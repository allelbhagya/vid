from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('play/<str:video_name>/', views.play_video, name='play_video'),
]
