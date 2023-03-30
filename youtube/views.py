from pytube import YouTube
import os
from rest_framework.decorators import api_view
from video_converter.utils import response, validate_body, validate_params
from threading import Thread
from .models import Youtube
from django.http import FileResponse

@api_view(['POST'])
def process_audio(request):
    if request.method == 'POST':
        is_valid = validate_body(request, ['url'])

        if is_valid:
            return is_valid
        
        url = request.data.get('url')

        if Youtube.objects.filter(url=url).exists():
            return response(data={'message': 'your request is ready', 'request_id': Youtube.objects.filter(url=url).first().id})
        
        youtube_obj = Youtube.objects.create(url=url, file_type='audio')
        Thread(target=download_audio, args=(url, youtube_obj)).start()

        return response(data={'message': 'your request is being processed', 'request_id': youtube_obj.id})

@api_view(['POST'])
def process_video(request):
    if request.method == 'POST':
        is_valid = validate_body(request, ['url'])

        if is_valid:
            return is_valid
        
        url = request.data.get('url')

        if Youtube.objects.filter(url=url).exists():
            return response(data={'message': 'your request is ready', 'request_id': Youtube.objects.filter(url=url).first().id})
        
        youtube_obj = Youtube.objects.create(url=url, file_type='video')
        Thread(target=download_video, args=(url, youtube_obj)).start()

        return response(data={'message': 'your request is being processed', 'request_id': youtube_obj.id})


@api_view(['GET'])
def check_status(request):
    if request.method == 'GET':
        is_valid = validate_params(request, ['request_id'])

        if is_valid:
            return is_valid

        request_id = request.query_params.get('request_id')
        youtube_obj = Youtube.objects.filter(id=request_id).first()

        if youtube_obj is None:
            return response(data={'message': f'Request with id {request_id} does not exist'}, status=404)

        return response(data={'request_id': request_id, 'title': youtube_obj.title ,'is_done': youtube_obj.is_done})

@api_view(['GET'])
def download_mp3(request):
    if request.method == 'GET':
        is_valid = validate_params(request, ['request_id'])

        if is_valid:
            return is_valid

        request_id = request.query_params.get('request_id')
        youtube_obj = Youtube.objects.filter(id=request_id).first()

        if youtube_obj is None:
            return response(data={'message': f'Request with id {request_id} does not exist'}, status=404)

        if youtube_obj.file_type != 'audio':
            return response(data={'message': f'Request with id {request_id} is not an audio request'}, status=400)

        if youtube_obj.is_done:
            file_object = youtube_obj.file_object
            file_response = FileResponse(file_object.open())
            file_response["Content-Length"] = file_object.size
            file_response["Content-Disposition"] = f"attachment; filename={youtube_obj.title}.mp3"
            return file_response
        else:
            return response(data={'message': f'Request with id {request_id} is still being processed'})

@api_view(['GET'])
def download_mp4(request):
    if request.method == 'GET':
        is_valid = validate_params(request, ['request_id'])

        if is_valid:
            return is_valid

        request_id = request.query_params.get('request_id')
        youtube_obj = Youtube.objects.filter(id=request_id).first()

        if youtube_obj is None:
            return response(data={'message': f'Request with id {request_id} does not exist'}, status=404)

        if youtube_obj.file_type != 'video':
            return response(data={'message': f'Request with id {request_id} is not a video request'}, status=400)

        if youtube_obj.is_done:
            file_object = youtube_obj.file_object
            file_response = FileResponse(file_object.open())
            file_response["Content-Length"] = file_object.size
            file_response["Content-Disposition"] = f"attachment; filename={youtube_obj.title}.mp4"
            return file_response
        else:
            return response(data={'message': f'Request with id {request_id} is still being processed'})

def download_video(url, youtube_obj):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    print(f"Title: {yt.title}")
    print("Downloading video...")
    video_file = video.download(output_path=os.path.join(os.getcwd(), 'output'))

    youtube_obj.title = yt.title
    youtube_obj.file_object = video_file
    youtube_obj.is_done = True
    youtube_obj.save()

    print("Successfully downloaded video!")

def download_audio(url, youtube_obj):
    yt = YouTube(url)
    video = yt.streams.filter(abr='160kbps', only_audio=True).first()
    print(f"Title: {yt.title}")
    print("Downloading audio...")
    audio_file = video.download(output_path=os.path.join(os.getcwd(), 'output'))

    base, ext = os.path.splitext(audio_file)
    new_file = f"{base}.mp3"
    os.rename(audio_file, new_file)

    youtube_obj.title = yt.title
    youtube_obj.file_object = new_file
    youtube_obj.is_done = True
    youtube_obj.save()

    print("Successfully downloaded audio!")





