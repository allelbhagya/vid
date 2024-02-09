import os
import cv2
from django.shortcuts import render, redirect
from django.conf import settings

def upload_video(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']
        # Save the uploaded video file
        with open(os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name), 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        
        # Convert the uploaded video to MPEG-4 AAC and H.264
        input_video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name)
        output_video_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'bw_' + video_file.name)
        if convert_video(input_video_path, output_video_path):
            return redirect('play_video', video_name='bw_' + video_file.name)
        else:
            return render(request, 'upload.html', {'error': 'Failed to convert video.'})
    
    return render(request, 'upload.html')

def play_video(request, video_name):
    video_url = os.path.join(settings.MEDIA_URL, 'videos', video_name)
    return render(request, 'play.html', {'video_url': video_url})

def convert_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return False
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Codec for MPEG-4 AAC
    fourcc_aac = cv2.VideoWriter_fourcc(*'mp4a')
    # Codec for H.264
    fourcc_h264 = cv2.VideoWriter_fourcc(*'avc1')
    
    # Use one of the above fourcc for output video
    out = cv2.VideoWriter(output_path, fourcc_h264, fps, (frame_width, frame_height), isColor=False) # Set isColor=False for grayscale
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert frame to black and white
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Write the frame
        out.write(frame_bw)
    
    cap.release()
    out.release()
    
    return True

def play_video(request):
    bw_videos = []
    video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    for filename in os.listdir(video_dir):
        if filename.startswith('bw_'):
            bw_videos.append(filename)
    
    return render(request, 'play_list.html', {'bw_videos': bw_videos})

def play_selected_video(request, video_name):
    video_url = os.path.join(settings.MEDIA_URL, 'videos', video_name)
    return render(request, 'play.html', {'video_url': video_url})
