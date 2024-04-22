# Dailynote Movie Maker

Takes in markdown files and creates a movie from them.

## Features

- **YouTube URL Handling:** If a Markdown file contains a YouTube URL (usually embedded), the tool adds the video as an audio track and plays the video in the background of the generated movie. Using [pytube](https://pytube.io/en/latest/).

- **Sequential Sentence Display:** Sentences from the Markdown files are shown one by one in the generated movie.
  ![](https://i.imgur.com/3rHbCaj.png)

- **Image Display:** If a sentence contains an image (typically within a footnote, "^[]"), it is displayed in the background. Images hosted online are directly used, while images linked to local files within the Obsidian vault are copied to a temporary folder and then used in the video.
  ![](https://i.imgur.com/131HV6k.png)
  (Still need to implement this feature)

- **Backlink Visualization:** Backlinks, indicated in the format "[[Joe Smith |Joe]]", are visually shown using their alias (e.g., "Joe") in a different color to signify their backlink status. Similarly, links in the format "[](url)" are treated similarly.
  ![](https://i.imgur.com/gz3v8jK.png)
  (Still need to implement this feature)

- **Title Card Customization:** The properties of the Markdown file, including thumbnail, note title, rating, and hidden status, are utilized for the title card of the video. The title card appears for a few seconds at the beginning and at the end of the video. Additionally, a faded transition is applied for a smoother appearance. Could possibly use [html2image](https://pypi.org/project/html2image/) to convert HTML to an image.
  (Still need to implement this feature)

![](https://i.imgur.com/n2Gcpzf.png)
Example of how the title card looks in the markdown using the `dataviewjs` snippet in combination with CSS and HTML.

The movie making process is done using [moviepy](https://pypi.org/project/moviepy/).
