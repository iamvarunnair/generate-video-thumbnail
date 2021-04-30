#!/usr/bin/env python
import os
import sys
import tempfile
from base64 import b64encode
from io import BytesIO, StringIO

from django.conf import settings
from django.conf.urls import url
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw

"""
 Usage:
    1. download this file tinydjango.py
    2. run `pip install django`
    3. run `python tinydjango.py runserver 8000`
    4. open a browser and head to http://localhost:8000
    5. bananas
"""

DEBUG = False

SECRET_KEY = '41+_$!j&y@zr#9cxdp6m9o3j&6dnk__bq*deii)5w6w744e7a#'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

TMPDIR = os.path.dirname(os.path.realpath(__file__))

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

"""
    Template with a form(with csrf token) to upload video files.
"""


@ensure_csrf_cookie
def uploadTemplate(request):
    return HttpResponse(
        f"<h1>Generate video preview and thumbnail<h1/>"
        f"<h4>Chose video file and click on 'Upload New Video' and that's it!</h4><br/>"
        f"<form enctype='multipart/form-data' action='/upload/' method='POST'>"
        f"<hr/><input type='file' name='video' accept='video/*'><br/><hr/><br/>"
        f"<button type='submit'> <h2><strong>Upload New Video</strong></h2> </button>"
        f"</form>")


"""
    View to handle the template form,
    generate thumbnail from video file and
    return a template with video and thumbnail preview.
"""


def uploadView(request):
    if request.method == 'POST':
        context = {
            # Converting InMemoryUploadedFile to base64 url data to bind to template video source tag.
            'video': b64encode(request.FILES['video'].read()).decode('utf-8'),
        }

        # creating a temporary video file, reading uploaded video file and writing it to temporary video file.
        with tempfile.NamedTemporaryFile(suffix='.mp4', dir=TMPDIR, delete=False) as destination:
            for chunk in request.FILES['video'].chunks():
                destination.write(chunk)
            # Loading the temporary video file into moviepy VideoFileClip class.
            clip = VideoFileClip(destination.name)
            # closing reading operation on temporary file just to be safe.
            destination.close()

        # clip.save_frame("thumbnail.jpg", t=1.00)      # if we want to save a thumbnail image file in current directory

        # get the first frame of temporary video file
        frame_data = clip.get_frame(1)
        # convert frame to an PIL Image object
        img = Image.fromarray(frame_data, 'RGB')
        # Generate thumbnail of size 300x300, although these are max values and aspect ratio of image is maintained.
        img.thumbnail((300, 300))

        # initiate a BytesIO buffer
        byte_io = BytesIO()
        # add image to buffer
        img.save(byte_io, 'PNG')

        # convert image to InMemoryUploadedFile format to store in django database
        imageFileObject = InMemoryUploadedFile(
            byte_io, None, 'test0.png', 'image/jpeg', byte_io.tell, None)
        # convert image into base64 url data to bind an image preview in src tag.
        imageBase64 = b64encode(byte_io.getvalue()).decode('utf-8')

        # close moviepy VideoFileClip class
        clip.close()
        # remove temporary video file from project directory
        os.remove(os.path.join(TMPDIR, destination.name))
    # return template
    return HttpResponse(
        f"<div style='display: flex; justify-content: space-evenly; align-items: flex-end'>"
        f"<div>"
        f"<h1>Uploaded Video:</h1><br/>"
        f"<video width='300' controls autoplay>"
        f"<source src='data:video/x-m4v;base64,{context['video']}' type='video/mp4'>"
        f"</video><br/>"
        f"</div>"
        f"<div>"
        f"<h3>Generated Thumbnail:</h3>"
        f"<img src='data:image/png;base64,{imageBase64}'>"
        f"</div>"
        f"</div>"
    )


urlpatterns = (
    url(r'^$', uploadTemplate, name='form'),
    url(r'^upload/$', uploadView, name='upload'),
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
