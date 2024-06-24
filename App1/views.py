from django.shortcuts import render, redirect
from django.http import HttpResponse
from pytube import YouTube
import os
import subprocess

def download_video(url):
    yt = YouTube(url)
    video_stream = yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first()
    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
    
    video_file = video_stream.download(filename='video.mp4')
    audio_file = audio_stream.download(filename='audio.mp4')

    ffmpeg_path = r"D:\ffmpeg-7.0.1-essentials_build\bin\ffmpeg.exe"

    sanitized_title = "".join(c for c in yt.title if c.isalnum() or c in (' ', '.', '_')).rstrip()
    output_file = os.path.join('static', f'{sanitized_title}.mp4')

    cmd = f'"{ffmpeg_path}" -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac "{output_file}"'
    subprocess.run(cmd, shell=True, check=True)

    os.remove(video_file)
    os.remove(audio_file)
    
    return output_file

def index(request):
    if request.method == 'POST':
        url = request.POST['url']
        try:
            output_file = download_video(url)
            return redirect('download')
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    return render(request, 'downloader/index.html')

def download(request):
    return render(request, 'downloader/download.html')
