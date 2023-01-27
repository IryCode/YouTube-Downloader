from pytube import YouTube
import ffmpeg


def userWant():
    choice = input("Select a format VIDEOS(V) AUDIOS(a) : ")
    if choice == "V":
        return "V"
    elif choice == "m":
        return "m"
    else:
        print("ERROR : YOU HAVE TO CHOICE BETWEEN VIDEOS or MUSICS")
        return userWant()


def getUrl():
    url = input("Enter the url : ")
    try:
        youtube_videos = YouTube(url)
        streams = youtube_videos.streams
    except:
        print("ERROR: This url is not valid or the video does not exist")
        return getUrl()
    else:
        return url


def percentage(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    print(f"Download progress ... {int(percent)}%")


url = getUrl()
youtube_videos = YouTube(url)
youtube_videos.register_on_progress_callback(percentage)
userchoice = userWant()

index = 1
if userchoice == "V":
    streams = youtube_videos.streams.filter( file_extension="mp4").order_by("resolution").desc()
    for stream in streams:
        print(f"{index} - {stream.resolution}")
        index += 1
else:
    streams = youtube_videos.streams.filter(type="audio").order_by("abr").desc()
    for stream in streams:
        print(f"{index} - {stream.abr}")
        index += 1


choice_num = int(input("Choose the quality : "))


itag = streams[choice_num - 1].itag

stream = streams.get_by_itag(itag)

print("Download start")
stream.download()
print("Download complete")