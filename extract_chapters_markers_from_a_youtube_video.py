import subprocess
import sys
import importlib
from datetime import timedelta
import os

def check_python():
    """Check if Python is installed and provide instructions if not."""
    try:
        python_version = subprocess.check_output([sys.executable, '--version'])
        print(f"Python is installed: {python_version.decode().strip()}")
    except FileNotFoundError:
        print("Python is not installed. Please install Python from https://www.python.org/ and try again.")
        sys.exit(1)

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def ensure_libraries():
    """Ensure required libraries are installed."""
    required_libraries = ['yt_dlp']
    for lib in required_libraries:
        try:
            importlib.import_module(lib)
        except ImportError:
            print(f"{lib} not found. Installing...")
            install(lib)

def format_time(seconds):
    """Convert seconds to a time format (hh:mm:ss)."""
    return str(timedelta(seconds=seconds))

def write_to_file(text, filename):
    """Write text to a file."""
    with open(filename, 'w') as file:
        file.write(text)

# Check if Python is installed
check_python()

# Ensure required libraries are installed
ensure_libraries()

import yt_dlp

# URL of the YouTube video
video_url = 'https://www.youtube.com/watch?v=V_xro1bcAuA'
base_link = video_url

output_text = ""

ydl_opts = {
    'skip_download': True,
    'extract_flat': True,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        chapters = info_dict.get("chapters", [])

        if chapters:
            for i in range(len(chapters)):
                chapter = chapters[i]
                start_time = chapter.get('start_time', 0)
                title = chapter.get('title', 'Untitled')
                end_time = chapters[i + 1]['start_time'] if i + 1 < len(chapters) else info_dict.get('duration', start_time)
                duration = end_time - start_time

                output_text += f"Chapter: {title}\n"
                output_text += f"Start time: {format_time(start_time)}\n"
                output_text += f"(Estimated chapter duration: {format_time(duration)})\n"
                output_text += f"Link: {base_link}&t={int(start_time)}s\n\n"
        else:
            output_text = "No chapters found."
except Exception as e:
    output_text = f"An error occurred: {e}"

# Define the filename and write to file
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'youtube_chapters_output.txt')

write_to_file(output_text, output_file)

print(f"Output written to {output_file}")
