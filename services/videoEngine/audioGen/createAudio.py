import json
import os
from dotenv import load_dotenv
import requests
import uuid

load_dotenv()


speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_url = os.getenv("AZURE_SPEECH_URL")


def generate_audio_ssml(narrator, voice, voiceStyle=None, rate=None, pitch=None, volume=None):
    # Start the base SSML structure
    ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">\n'
    
    # Add the voice
    ssml += f'  <voice name="{voice}">\n'

    # If voiceStyle is provided, include it with mstts:express-as
    if voiceStyle:
        ssml += f'    <mstts:express-as style="{voiceStyle}">\n'
    
    # Add prosody tag with optional parameters (rate, pitch, and volume)
    prosody_opening = '      <prosody'
    if rate:
        prosody_opening += f' rate="{rate}"'
    if pitch:
        prosody_opening += f' pitch="{pitch}"'
    if volume:
        prosody_opening += f' volume="{volume}"'
    
    prosody_opening += '>\n'
    ssml += prosody_opening

    # Insert the actual narration content
    ssml += f'        {narrator}\n'

    # Close prosody and express-as (if used)
    ssml += '      </prosody>\n'
    if voiceStyle:
        ssml += '    </mstts:express-as>\n'

    # Close the voice and speak tags
    ssml += '  </voice>\n</speak>'



def generate_audio_azure(input_json):
    # Set up directory to save audio files
    audio_dir_name = "audio"
    audio_dir = os.path.join(os.curdir, audio_dir_name)

    # Create the directory if it doesn't exist
    if not os.path.isdir(audio_dir):
        os.mkdir(audio_dir)

    input_json = json.loads(input_json)

    # Load the narrator data from the input JSON
    scenes = input_json["storyboard"]

    # Iterate over each scene in the storyboard
    for scene in scenes:
        id = scene["id"]
        narrator_text = scene.get("narrator", None)
        voice = scene.get("voice", "en-US-AdamMultilingualNeural")  # default voice
        voice_style = scene.get("voiceStyle", "general")  # default style if not provided
        rate = scene.get("rate", "medium")  # default rate
        pitch = scene.get("pitch", "medium")  # default pitch
        volume = scene.get("volume", "medium")  # default volume

        if narrator_text:
            # Generate SSML including the volume parameter
            ssml = generate_audio_ssml(
                narrator=narrator_text,
                voice=voice,
                voiceStyle=voice_style,
                rate=rate,
                pitch=pitch,
                volume=volume
            )

            # Define headers for Azure API request
            headers = {
                "Ocp-Apim-Subscription-Key": speech_key,
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
                "User-Agent": "python-requests"
            }

            # Send the SSML to Azure API
            print(f"Generating audio for scene {id}: {narrator_text}")
            response = requests.post(speech_url, headers=headers, data=ssml)

            # Save the audio file if the request is successful
            if response.status_code == 200:
                audio_bytes = response.content

                # Create a unique filename and save the audio
                unique_id = uuid.uuid4().hex[:8]
                generated_audio_name = f"scene_{id}_{unique_id}.mp3"
                generated_audio_filepath = os.path.join(audio_dir, generated_audio_name)
                with open(generated_audio_filepath, "wb") as audio_file:
                    audio_file.write(audio_bytes)

                # Update the JSON with the file path
                scene["audio_file_name"] = generated_audio_name
            else:
                print(f"Error generating audio for scene {id}: {response.status_code}, {response.text}")

    # Return the updated JSON
    return input_json