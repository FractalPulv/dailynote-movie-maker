import os
import re
import ssl
from tkinter import Tk, filedialog, Listbox, Scrollbar, Button, Label, Text
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from pytube import YouTube
from scripts.audio_downloader import download_audio_from_youtube
from scripts.video_generator import generate_video
from scripts.text_extractor import extract_text, extract_front_matter

ssl._create_default_https_context = ssl._create_stdlib_context

from dotenv import load_dotenv

load_dotenv()

DIR_PATH = os.getenv('DIR_PATH')

# Function to handle file selection
def load_selected_file(event):
    selection_index = file_listbox.curselection()
    if selection_index:
        file_name = file_listbox.get(selection_index)
        file_path = os.path.join(directory_path, file_name)
        load_content(file_path)

# Function to load content from selected file
def load_content(file_path):
    with open(file_path, 'r') as file:
        note_content = file.read()
        front_matter = extract_front_matter(note_content)
        front_matter_text.config(state='normal')
        front_matter_text.delete('1.0', 'end')
        front_matter_text.insert('1.0', front_matter)
        front_matter_text.config(state='disabled')
        generate_button.config(state='normal')
        global selected_file_path
        selected_file_path = file_path

# Function to generate the video
def generate_video_from_selected_file():

    template_path = './template_daily.md'
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
        match = re.search(r'```(.*?)```', template_content, re.DOTALL)
        if match:
            dataview = match.group(1)
        else:
            dataview = ''

    with open(selected_file_path, 'r') as file:
        note_content = file.read()
        front_matter = extract_front_matter(note_content)
        after_dataview_match = re.search(re.escape(dataview) + r'(.*)', note_content, re.DOTALL)
        if after_dataview_match:
            note_content = after_dataview_match.group(1)
        text_content = extract_text(note_content)
        youtube_match = re.search(r'<iframe.*?src="(.*?)".*?>', text_content)
        if youtube_match:
            youtube_url = youtube_match.group(1)
            audio = download_audio_from_youtube(youtube_url)
            if audio:
                generate_video(text_content, front_matter, audio)
            else:
                print("Failed to download audio from YouTube.")
        else:
            print("No YouTube video found.")

# Initialize tkinter window
window = Tk()
window.title("Video Generator")
window.geometry("600x400")

# Specify the directory path
directory_path = DIR_PATH

# Label for file list
file_label = Label(window, text="Select a file:")
file_label.pack()

# Create listbox widget to display files
file_listbox = Listbox(window, width=15, height=100)  # Increase the height of the listbox
file_listbox.pack(side="left")

# Add scrollbar to the listbox
scrollbar = Scrollbar(window, orient="vertical")
scrollbar.config(command=file_listbox.yview)
scrollbar.pack(side="left", fill="y")

file_listbox.config(yscrollcommand=scrollbar.set)

# Add files to the listbox
for file_name in sorted(os.listdir(directory_path)):
    if file_name.endswith(".md"):
        file_listbox.insert("end", file_name)

# Bind event to load selected file
file_listbox.bind("<<ListboxSelect>>", load_selected_file)

# Label for front matter
front_matter_label = Label(window, text="Front Matter:")
front_matter_label.pack()

# Text widget to display front matter
front_matter_text = Text(window, height=10, width=60, wrap='word', state='disabled')
front_matter_text.pack()

# Button to generate video
generate_button = Button(window, text="Generate Video", command=generate_video_from_selected_file, state='disabled')
generate_button.pack()

window.mainloop()
