# Generate Video Thumbnails

#

#### _Upload thubnail from a html form and generate a thumbnail, preview, store it as a file or Uploaded file._

#

#

## Features

A minimal django project with two templates:

-   Upload the video on the first template and press upload
-   Preview uploaded video and genereated thumbnail

Algorithm logic:

-   The video is read from the uploaded form, and temporarily stored in project directory
-   The temporarily stored video file is read and a new PIL Image is created from the first frame of the video
-   From the new PIL Image
    -   we can store the image in the project directory
    -   upload as uploaded file(blob/InMemoryUploadedFile) into database
    -   convert into base64 image url to preview in template
-   Once done, delete the temporary video file in directory
-   ✨Magic ✨

#

#

## Tech

Dependencies used

-   [Django](djangoproject.com)
-   [Moviepy](pypi.org/project/moviepy)
-   [Requests](pypi.org/project/requests)
-   [Ffmpeg](ffmpeg.org) - installed on the system and added to environment path/system path
-   [Virtualenvwrapper](pypi.org/project/virtualenvwrapper)

#

#

## Installation

Dillinger requires [Python 3](python.org) to run.

#

Create virtual environment

```sh
mkvirtualenv <env_name>
```

List all virtualenvwrappers in system

```sh
lsvirtualenv
```

Start virtual environment

```sh
workon <env_name>
```

Install dependencies in virtual environment

```sh
pip install -r requirements.txt
```

Run django server on port 8000

```sh
py tint_django.py runserver 8000
```

Close when done with running the program

```sh
workon <env_name>
```

#

#

**Hope you like it!**
