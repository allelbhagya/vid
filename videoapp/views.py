from django.shortcuts import render, redirect
from django.conf import settings
import os
import cv2

def upload_video(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']
        # Save the uploaded video file
        with open(os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name), 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        
        # Convert the uploaded video to black and white
        input_video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name)
        output_video_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'bw_' + video_file.name)
        if convert_to_bw(input_video_path, output_video_path):
            return redirect('play_video', video_name='bw_' + video_file.name)
        else:
            return render(request, 'upload.html', {'error': 'Failed to convert video to black and white.'})
    
    return render(request, 'upload.html')

def play_video(request, video_name):
    video_url = os.path.join(settings.MEDIA_URL, 'videos', video_name)
    return render(request, 'play.html', {'video_url': video_url})

def convert_to_bw(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return False
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)  # isColor=False for grayscale
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(frame_bw)
    
    cap.release()
    out.release()
    
    return True