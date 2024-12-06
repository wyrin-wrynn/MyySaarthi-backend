import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def transcribeAudioFile(audio_file_path):
    # Ensure the audio file path exists
    if not os.path.isfile(audio_file_path):
        print(f"Audio file '{audio_file_path}' not found.")
        return None
    
    # Open the audio file and request transcription
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    
    # Parse transcription to create an array of dictionaries for each word
    output = transcript.words
    transcription_array = []
    for word in output:
        tempObj = {
            'start': round(float(word.start), 2),
            'end': round(float(word.end), 2),
            'word': word.word
        }
        transcription_array.append(tempObj)
    
    return transcription_array

def createTranscription(data):
    for scene in data:
        audio_file_path = scene.get("audio_file")
        
        # Get transcription array by calling transcribeAudioFile function
        transcription_array = transcribeAudioFile(audio_file_path)
        
        if transcription_array is not None:
            # Add the transcription array to the scene
            scene["transcription"] = transcription_array

    return True