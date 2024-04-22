import re
import os
from tkinter import Tk, filedialog
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from pytube import YouTube
import ssl

from scripts.audio_downloader import download_audio_from_youtube
from scripts.video_generator import generate_video
from scripts.text_extractor import extract_text, extract_front_matter


ssl._create_default_https_context = ssl._create_stdlib_context


# Import any other necessary libraries for audio extraction (e.g., pytube)




# Read the content of the template file to extract the dataview
template_path = './template_daily.md'
with open(template_path, 'r') as template_file:
    template_content = template_file.read()
    match = re.search(r'```(.*?)```', template_content, re.DOTALL)
    if match:
        dataview = match.group(1)
    else:
        dataview = ''

# Prompt the user to select a file
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Read the content of the selected file
with open(file_path, 'r') as file:
    note_content = file.read()

front_matter = extract_front_matter(note_content)


# Extract the text after the template dataview match
after_dataview_match = re.search(re.escape(dataview) + r'(.*)', note_content, re.DOTALL)
if after_dataview_match:
    note_content = after_dataview_match.group(1)

# Extract text content from the note
text_content = extract_text(note_content)
print("=== Text Content ===")
print(text_content)
print("====================")

# Check if there's a YouTube video embedded in the text
youtube_match = re.search(r'<iframe.*?src="(.*?)".*?>', text_content)
if youtube_match:
    youtube_url = youtube_match.group(1)
    print("YouTube video found:", youtube_url)
    # Download audio from the YouTube video
    audio = download_audio_from_youtube(youtube_url)
    # Once you have the audio, you can proceed to generate the video with the text content and audio.
else:
    print("No YouTube video found.")

# Generate a video with the extracted text content and audio
if audio:
    generate_video(text_content, front_matter, audio)
else:
    generate_video(text_content, front_matter)


# 2024-04-05