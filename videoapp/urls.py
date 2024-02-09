from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('play/', views.play_video, name='play_video'),  # Route for listing black and white videos
    path('play/<str:video_name>/', views.play_selected_video, name='play_selected_video'),  # Route for playing selected video
]
