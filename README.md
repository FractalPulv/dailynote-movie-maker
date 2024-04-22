# Dailynote Movie Maker
Takes in markdown files and creates a movie from them.

## Features
   - **YouTube URL Handling:** If a Markdown file contains a YouTube URL (usually embedded), the tool adds the video as an audio track and plays the video in the background of the generated movie.

   - S**equential Sentence Display:** Sentences from the Markdown files are shown one by one in the generated movie.

   - **Image Display:** If a sentence contains an image (typically within a footnote, "^[]"), it is displayed in the background. Images hosted online are directly used, while images linked to local files within the Obsidian vault are copied to a temporary folder and then used in the video.

   - **Backlink Visualization:** Backlinks, indicated in the format "[[Joe Smith |Joe]]", are visually shown using their alias (e.g., "Joe") in a different color to signify their backlink status. Similarly, links in the format "" are treated similarly.

   - **Title Card Customization:** The properties of the Markdown file, including thumbnail, note title, rating, and hidden status, are utilized for the title card of the video. The title card appears for a few seconds at the beginning and at the end of the video. Additionally, a faded transition is applied for a smoother appearance.