import os
import edge_tts
import asyncio
import uuid
import json

# Default voice configuration
DEFAULT_VOICE = "en-US-AndrewMultilingualNeural"
AUDIO_DIR = "/root/AIVideos/data/audio"  # Absolute path to the save location

# Ensure the audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

# Async function to generate audio with edge-tts
async def generate_audio_simple(text,id=0, voice=DEFAULT_VOICE):
    tts = edge_tts.Communicate(text, voice)
    unique_id = uuid.uuid4().hex[:8]
    generated_audio_name = f"audio_{id}_{unique_id}.mp3"
    generated_audio_filepath = os.path.join(AUDIO_DIR, generated_audio_name)
    await tts.save(generated_audio_filepath)
    return generated_audio_filepath

# Wrapper function to handle audio generation and update JSON with audio file paths
def create_audio_for_narrations(json_data, voice=DEFAULT_VOICE):
    async def process_scenes(data):
        for scene in data:
            id = scene['id']
            narration_text = scene.get("narration", "")
            if narration_text:
                # Generate audio file for the narration
                audio_file_path = await generate_audio_simple(narration_text, id,voice)
                # Add audio file path to the JSON structure
                scene["audio_file"] = audio_file_path

    # Run the async process in an event loop
    asyncio.run(process_scenes(json_data))



