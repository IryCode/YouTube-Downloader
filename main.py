from pytube import YouTube
from termcolor import colored
import ffmpeg
import os


def userWant():
    choice = input("Select a format ; VIDEOS(V) AUDIOS(a) : ")
    if choice == "V":
        return "V"
    elif choice == "a":
        return "a"
    else:
        print(colored("ERROR : YOU HAVE TO CHOICE BETWEEN VIDEOS or AUDIOD", "red"))
        return userWant()


def getUrl():
    url = input(colored("Enter the YouTube video url : ", "blue"))
    try:
        youtube_videos = YouTube(url)
        youtube_videos.title
    except:
        print(colored("ERROR: This url is not valid or the video does not exist", "red"))
        return getUrl()
    else:
        return url


def percentage(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    print(colored(f"Download progress ... ", "cyan") + colored(f"{int(percent)}%", "green"))


url = getUrl()
youtube_video = YouTube(url)
print(f"TITLE : {youtube_video.title}")
youtube_video.register_on_progress_callback(percentage)

userFormat = userWant()

streams = youtube_video.streams.filter(type="audio", file_extension="mp4").order_by("abr").desc()
audio_stream = streams[0]

streams = youtube_video.streams.filter(type="video", file_extension="mp4").order_by("resolution").desc()
video_stream = streams[0]

if userFormat == "a":
    print(colored("Downloading audio", "cyan"))
    audio_stream.download("audio")
    print(colored("Audio Downloaded", "green"))
else:
    print(colored("Download video", "cyan"))
    video_stream.download("video")
    print(colored("Video download complete", "green"))

    print(colored("Download audio", "cyan"))
    audio_stream.download("audio")
    print(colored("Audio download complete", "green"))

    audio_filename = os.path.join("audio", video_stream.default_filename)
    video_filename = os.path.join("video", video_stream.default_filename)
    output_filename = video_stream.default_filename

    print(colored("File combination", "cyan"))
    ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename, vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)
    print(colored("Combination complete", "green"))

    os.remove(audio_filename)
    os.remove(video_filename)
    os.rmdir("audio")
    os.rmdir("video")
