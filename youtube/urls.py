from django.urls import path
from youtube.views import *

app_name = "youtube"

urlpatterns = [
    path("process_audio", process_audio, name="process_audio"),
    path("process_video", process_video, name="process_video"),
    path("status", check_status, name="tatus"),
    path("download_mp3", download_mp3, name="download_mp3"),
    path("download_mp4", download_mp4, name="download_mp4"),
]