import yt_dlp
import requests
import os
import uuid
import glob
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
import math


# Load API key and headers from .env file
load_dotenv()
API_URL = os.getenv("API_URL_WHISPER")
HF_KEY = os.getenv("HF_KEY")
headers = {"Authorization": HF_KEY}

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)



# Define the temp folder as a relative path within the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FOLDER = os.path.join(SCRIPT_DIR, "../data/temp")

# Ensure the temp folder exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

def download_audio(url):
    # Generate a unique temporary filename (without extension) in the specified temp folder
    temp_filename = os.path.join(TEMP_FOLDER, f"temp_{uuid.uuid4().hex}")
    
    ydl_opts = {
        'format': 'bestaudio/best',  # Try to download the best available audio quality
        'extract_audio': True,       # Only extract audio
        'audio_format': 'mp3',       # Convert to mp3 format
        'outtmpl': temp_filename,    # Use temporary filename in the specified temp folder
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Set quality in kbps (optional)
        }],
        'cookiefile': 'services/videoSummarize/cookies.txt',  # Path to your cookies file
        'noplaylist': True,          # Ensure only a single video is downloaded if the URL contains a playlist
        'ignoreerrors': True,        # Continue with other formats if an error occurs
        'prefer_ffmpeg': True,       # Prefer ffmpeg for postprocessing
        'quiet': False,              # Print logs to debug issues (remove for production)
        'verbose': True,             # Enable verbose output for debugging (remove for production)
        'restrictfilenames': True,   # Avoid special characters in filenames
    }



    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'Unknown Title')
        print(f"Title: {title}")
        ydl.download([url])

    # Find the generated .mp3 file in the temp folder with glob
    final_filename = glob.glob(f"{temp_filename}*.mp3")
    if not final_filename:
        raise FileNotFoundError(f"No .mp3 file found for {temp_filename}")
    
    # Return title and the first matching .mp3 filename
    return title, final_filename[0]

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    response.raise_for_status()  # Check if request was successful
    return response.json()

def openaiWhisper(filename):
    max_file_size = 10485760  # 10 MB in bytes

    # Step 1: Check file size
    file_size = os.path.getsize(filename)
    print(f"Original file size: {file_size} bytes")

    if file_size <= max_file_size:
        print("File size is within the limit. Proceeding with transcription.")
        with open(filename, "rb") as audio_file:
            transcript = client.audio.translations.create(
                file=audio_file,
                model="whisper-1"
            )
        print(f"Transcription complete for the original file: {transcript.text}")
        return transcript.text

    # Step 2: Split the file into proportional chunks
    print("File size exceeds limit. Splitting the file into chunks...")
    audio = AudioSegment.from_file(filename, format="mp3")
    duration_ms = len(audio)
    print(f"Total audio duration: {duration_ms} milliseconds")

    # Calculate the number of chunks needed
    num_chunks = math.ceil(file_size / max_file_size)
    print(f"Splitting the file into {num_chunks} chunks...")

    # Calculate duration per chunk
    chunk_duration_ms = math.ceil(duration_ms / num_chunks)
    print(f"Chunk duration: {chunk_duration_ms} milliseconds")

    # Create chunks based on equal duration splits
    chunks = []
    start_ms = 0

    for i in range(num_chunks):
        end_ms = min(start_ms + chunk_duration_ms, duration_ms)
        print(f"Creating chunk {i} from {start_ms} to {end_ms} milliseconds")
        chunk = audio[start_ms:end_ms]

        chunk_filename = f"temp_chunk_{i}.mp3"
        chunk.export(chunk_filename, format="mp3", bitrate="192k")
        print(f"Exported chunk {i} to {chunk_filename}")

        chunks.append(chunk_filename)
        start_ms = end_ms

    # Step 3: Process each chunk
    results = []
    for i, chunk_filename in enumerate(chunks):
        print(f"Transcribing chunk {i} from {chunk_filename}...")
        with open(chunk_filename, "rb") as audio_file:
            transcript = client.audio.translations.create(
                file=audio_file,
                model="whisper-1"
            )
        chunk_text = transcript.text
        print(f"Transcription for chunk {i}: {chunk_text}")
        results.append(chunk_text)
        os.remove(chunk_filename)  # Clean up temp file
        print(f"Deleted temporary file {chunk_filename}.")

    # Step 4: Concatenate results
    print("Concatenating all transcriptions...")
    full_transcription = " ".join(results)
    print("Transcription process complete.")
    return full_transcription

def get_source(url):
    # Step 1: Download audio and get title
    title, final_filename = download_audio(url)
    
    # Step 2: Transcribe using Whisper API
    transcription_response = openaiWhisper(final_filename)

    # Step 3: Clean up intermediate file
    if os.path.exists(final_filename):
        os.remove(final_filename)

    # Step 4: Return result as JSON
    return {'title': title, 'body': transcription_response}

# Example usage
#video_url = "https://www.youtube.com/watch?v=fLu080UX25o"
#output = transcribe_youtube_audio(video_url)
#print(output)

