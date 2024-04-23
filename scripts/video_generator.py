from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
import re
import requests
from PIL import Image
from io import BytesIO


# Define a method for generating a video with text content and audio
def generate_video(text_content, front_matter, audio=None):
    # Define video parameters
    duration = 20  # Duration of the video in seconds
    fps = 10  # Frames per second

    # Create title card using front matter
    # create_title_card(front_matter) commented out for now =====================

    # Find all images in the text content
    images = re.findall(r'\!\[(.*?)\]\((.*?)\)', text_content)

    # Create a list to store all image URLs
    image_urls = [url for _, url in images]

    # Download and process images
    background_clips = []
    for image_url in image_urls:
        # Download the image and convert it to a moviepy clip
        response = requests.get(image_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            try:
                # Attempt to open the image
                image = Image.open(BytesIO(response.content))
                bg_clip = TextClip("", color='white', bg_color='black', size=(image.width, image.height)).set_duration(duration)
                bg_clip = bg_clip.set_mask(image).set_opacity(0.5)
                background_clips.append(bg_clip)
            except Exception as e:
                print(f"Error processing image from {image_url}: {e}")
        else:
            print(f"Failed to download image from {image_url}. Status code: {response.status_code}")


    # Split the text_content into an array of sentences separated by '. ' or '.\n'
    sentences = re.split(r'\. |\.\n', text_content)

    # Create an empty list to store the text clips
    text_clips = []

    # Iterate over each sentence and create a text clip
    for sentence in sentences:
        # Check if the sentence contains a footnote with an image
        match = re.search(r'\^\[\!\[(.*?)\]\((.*?)\)\]', sentence)
        if match:
            # Extract the URL of the image from the footnote
            image_url = match.group(2)
            
            # Download the image and convert it to a moviepy clip
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            bg_clip = TextClip(sentence, fontsize=70, color='white', bg_color='black', size=(1920, 1080), method='caption', align='center', stroke_color='black', stroke_width=3)
            bg_clip = bg_clip.set_duration(5).set_position(('center', 'center')).set_opacity(0.5)
            bg_clip = bg_clip.set_mask(image)
            
            # Add the background clip to the list
            background_clips.append(bg_clip)
        else:
            # Create a text clip for the current sentence
            txt_clip = TextClip(sentence, fontsize=70, color='white', bg_color='black', size=(1920, 1080), method='caption', align='center', stroke_color='black', stroke_width=3)

            # Set the duration of the text clip to 5 seconds
            txt_clip = txt_clip.set_duration(5)

            # Add the text clip to the list
            text_clips.append(txt_clip)

    # Concatenate all text clips
    final_text_clip = concatenate_videoclips(text_clips)

    if background_clips:
        # Concatenate all background clips
        final_background_clip = concatenate_videoclips(background_clips)

        # Combine text and background clips
        final_clip = CompositeVideoClip([final_text_clip.set_position('center'), final_background_clip])
    else:
        # No background clips found, use only text clip
        final_clip = final_text_clip.set_position('center')

    if audio:
        # Create an audio clip from the downloaded audio
        audio_clip = AudioFileClip(audio)

        # Set the duration of the audio clip
        audio_clip = audio_clip.set_duration(duration)

        # Set audio volume to 0 during text appearance
        audio_clip = audio_clip.volumex(0.2).set_start(0).set_end(5 * len(sentences))

        # Combine the video clip and audio clip
        final_clip = CompositeVideoClip([final_clip.set_audio(audio_clip)])

    # Write the video file to disk
    final_clip.write_videofile('./output.mp4', fps=fps)



# Define a function to take the front matter and create a title card
# An example front matter could be:
# rating: "~"
# entry_title: The day I saw Kris
# hidden: false
# entry_thumbnail: https://i.imgur.com/5AyRLQD.jpeg
# 
# I want the entry_title to be displayed in the center of the screen with a background image from entry_thumbnail and the rating symbol. If hidden then show a lock emoji.
# Define a function to take the front matter and create a title card
def create_title_card(front_matter):
    # Extract the entry_title from the front matter
    match = re.search(r'entry_title: (.*?)\n', front_matter)
    if match:
        entry_title = match.group(1)
    else:
        entry_title = "Daily note" # Or Untitled

    # Extract the entry_thumbnail from the front matter
    match = re.search(r'entry_thumbnail: (.*?)\n', front_matter)
    if match:
        entry_thumbnail = match.group(1)
    else:
        entry_thumbnail = ""

    # Extract the rating from the front matter
    match = re.search(r'rating: (.*?)\n', front_matter)
    if match:
        rating = match.group(1)
    else:
        rating = ""

    # Extract the hidden status from the front matter
    match = re.search(r'hidden: (.*?)\n', front_matter)
    if match:
        hidden = match.group(1)
    else:
        hidden = ""

    print("Entry Title:", entry_title)
    print("Entry Thumbnail:", entry_thumbnail)
    print("Rating:", rating)
    print("Hidden:", hidden)

    # Create a title card with the entry title, thumbnail, rating, and hidden status
    title_clip = TextClip(entry_title, fontsize=70, color='white', bg_color='black', size=(1920, 1080), method='caption', align='center', stroke_color='black', stroke_width=3)
    if entry_thumbnail:
        # Download the image and convert it to a moviepy clip
        response = requests.get(entry_thumbnail)
        image = Image.open(BytesIO(response.content))
        title_clip = title_clip.set_mask(image) # Set image as mask
        
        # Create a transparent clip of the same size as the text clip and use it as a mask
        transparent_clip = TextClip("", size=title_clip.size, color=(0, 0, 0, 0))
        title_clip = title_clip.set_mask(transparent_clip)
        
    if rating:
        # Create a transparent clip of the same size as the text clip and use it as a mask for rating
        transparent_clip = TextClip("", size=title_clip.size, color='white')  # Adjusted here
        rating_clip = TextClip(rating, fontsize=70, color='white', bg_color='black', size=(1920, 1080), method='caption', align='center', stroke_color='black', stroke_width=3)
        rating_clip = rating_clip.set_mask(transparent_clip)
        
        # Overlay rating on title clip
        title_clip = CompositeVideoClip([title_clip, rating_clip.set_position(('center', 'bottom'))])

    if hidden == "true":
        # Create a lock emoji clip
        lock_clip = TextClip("🔒", fontsize=70, color='white', bg_color='black', size=(1920, 1080), method='caption', align='center', stroke_color='black', stroke_width=3)
        title_clip = CompositeVideoClip([title_clip, lock_clip.set_position(('center', 'top'))])

    # Write the title card to disk
    title_clip.write_videofile('./title_card.mp4', fps=1, codec='libx264', audio=False)
