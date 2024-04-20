from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
import re
import requests
from PIL import Image
from io import BytesIO

# Define a method for generating a video with text content and audio
def generate_video(text_content, audio=None):
    # Define video parameters
    duration = 20  # Duration of the video in seconds
    fps = 10  # Frames per second

    # Split the text_content into an array of sentences separated by '. ' or '.\n'
    sentences = re.split(r'\. |\.\n', text_content)

    # Create an empty list to store the text clips
    text_clips = []

    # Create an empty list to store background clips (images)
    background_clips = []

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
