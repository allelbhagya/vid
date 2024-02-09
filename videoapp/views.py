from django.shortcuts import render, redirect
from django.conf import settings
import os

def upload_video(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']
        # Save the uploaded video file
        with open(os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name), 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        return redirect('play_video', video_name=video_file.name)
    return render(request, 'upload.html')

def play_video(request, video_name):
    video_url = os.path.join(settings.MEDIA_URL, 'videos', video_name)
    return render(request, 'play.html', {'video_url': video_url})
