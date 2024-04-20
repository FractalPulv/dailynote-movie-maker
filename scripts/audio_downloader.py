import os
from pytube import YouTube

# Define a method for downloading audio from YouTube
def download_audio_from_youtube(youtube_url):
    # Download audio from YouTube using pytube
    yt = YouTube(youtube_url)
    video = yt.streams.filter(only_audio=True).first() 
  
    # Set the destination folder to "./audio"
    destination = "../audio"
    
    # download the file 
    out_file = video.download(output_path=destination) 
    
    # save the file as audio.mp3
    new_file = os.path.join(destination, "audio.mp3")
    os.rename(out_file, new_file) 
    
    # result of success 
    print(yt.title + " has been successfully downloaded.")

    return new_file