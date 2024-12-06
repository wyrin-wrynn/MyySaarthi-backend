from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from services.videoEngine.scriptGen import prompts
import os
from dotenv import load_dotenv
import re

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


class PicBox(BaseModel):
    id: str
    image: str
    narration_chunk: str
    scene_id: str


class Scene(BaseModel):
    picbox: List[PicBox]



# Helper function to standardize strings and check/remove substring
def standardize_string(input_string):
    input_string = re.sub(r'[^\w\s]', '', input_string)  # Remove punctuation
    input_string = re.sub(r'\s+', ' ', input_string).strip()  # Remove extra spaces
    return input_string.lower()

def remove_substring_if_exists(main_string, substring):
    standardized_main = standardize_string(main_string)
    standardized_sub = standardize_string(substring)
    
    if standardized_sub in standardized_main:
        standardized_main = standardized_main.replace(standardized_sub, "", 1).strip()
        return standardized_main
    else:
        return None  # Indicate that the substring was not found

def get_chunk_positions(main_narration, chunks):
    """Helper function to get start positions of each chunk in main_narration."""
    positions = []
    for chunk in chunks:
        standardized_main = standardize_string(main_narration)
        standardized_chunk = standardize_string(chunk['narration_chunk'])
        start_idx = standardized_main.find(standardized_chunk)
        if start_idx != -1:
            positions.append((start_idx, chunk))
    # Sort chunks based on their appearance order in main_narration
    positions.sort(key=lambda x: x[0])
    return [chunk for _, chunk in positions]

def generate_storyboard(script):
    client = OpenAI(api_key=api_key)
    picbox = []
    
    max_retries = 10  # Maximum attempts for regenerating a scene
    i = 1
    
    for scene in script:
        retry_count = 0
        scene_generated = False  # Flag to track if scene was generated successfully
        
        while retry_count < max_retries and not scene_generated:
            print(f"Processing Scene {i} (Attempt {retry_count + 1})")
            retry_count += 1

            # Construct the prompt for each scene
            prompt = prompts.generate_storyboard_prompt
            
            # Form the user's message for the scene
            user_message = (
                f"Scene ID: {scene['id']}\n"
                f"Narration: {scene['narration']}\n"
                f"Tone: {scene['tone']}\n"
                f"Theme: {scene['theme']}\n"
                f"Emotions: {scene['emotions']}\n"
            )

            # Additional instruction if this is a retry and there was leftover narration
            feedback_message = None
            if retry_count > 1 and main_narration.strip():
                feedback_message = (
                    f"Please note: The following part of the narration was not covered last time: "
                    f"\"{main_narration.strip()}\""
                )
                print(f"Retrying with additional instruction: {feedback_message}")
            
            # Construct the message array for the API call
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
            if feedback_message:
                messages.append({"role": "user", "content": feedback_message})
            
            try:
                # Make an API call for each scene
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",  # Adjust model name as required
                    messages=messages,
                    response_format=Scene  # Using structured format parsing here for clarity
                )
                
                # Access the picbox directly from parsed
                scene_picbox = completion.choices[0].message.parsed.picbox
                
                # Temporary list to store this scene's valid pics
                temp_picbox = []
                
                # Work with a copy of the main narration
                main_narration = scene['narration']
                
                # Verify if all narration chunks cover the full narration
                for pic in scene_picbox:
                    # Check if narration_chunk exists in main_narration
                    new_narration = remove_substring_if_exists(main_narration, pic.narration_chunk)
                    
                    # If new_narration is None, skip adding this pic
                    if new_narration is not None:
                        # Update main_narration and add pic to temp_picbox
                        main_narration = new_narration
                        temp_picbox.append({
                            "id": pic.id,
                            "image": pic.image,
                            "narration_chunk": pic.narration_chunk,
                            "scene_id": pic.scene_id
                        })
                
                # Check if all chunks were processed, otherwise retry
                if main_narration.strip() == "":
                    # Verify and correct chunk order based on positions
                    ordered_picbox = get_chunk_positions(scene['narration'], temp_picbox)
                    picbox.extend(ordered_picbox)  # Add ordered chunks to final picbox
                    scene_generated = True  # Mark this scene as successfully generated
                else:
                    # Log details when retrying
                    print(f"Scene {scene['id']} incomplete on attempt {retry_count}. Remaining narration: '{main_narration}'")
                    print(f"Chunks generated so far:")
                    for pic in temp_picbox:
                        print(f" - ID: {pic['id']}, Narration Chunk: '{pic['narration_chunk']}', Scene ID: {pic['scene_id']}")
                    print("Retrying...\n")

            except Exception as e:
                print(f"Error processing scene ID {scene['id']} on attempt {retry_count}: {str(e)}")
                return {"error": f"Failed to process scene ID {scene['id']}: {str(e)}"}
        
        if not scene_generated:
            print(f"Scene ID {scene['id']} could not be generated successfully after {max_retries} attempts.")
            return {"error": f"Scene ID {scene['id']} could not be generated successfully after {max_retries} attempts."}
        
        i += 1

    print("Storyboard created and cleaned successfully.")
    return picbox