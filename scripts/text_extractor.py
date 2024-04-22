import re

# Define a function to extract text from note content
def extract_text(note_content):
    # Remove front matter (YAML metadata)
    note_content = re.sub(r'^---[\s\S]+?---', '', note_content)

    # Extract text content
    text_content = note_content.strip()  # Trim leading/trailing whitespace
    return text_content

# Define a function to save the front matter (YAML metadata) of a note (between '---' delimiters)
def extract_front_matter(note_content):
    # Extract front matter (YAML metadata)
    match = re.search(r'^---([\s\S]+?)---', note_content)
    if match:
        front_matter = match.group(1).strip()  # Trim leading/trailing whitespace
        print("=== Front Matter ===")
        print(front_matter)  # Print the front matter
        print("====================")
    else:
        front_matter = ''
        print("No front matter found.")
    return front_matter