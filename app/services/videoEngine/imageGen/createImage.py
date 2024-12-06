import os
import json
import requests
from dotenv import load_dotenv
import uuid
import time

# Load API key and headers from .env file
load_dotenv()
API_URL = os.getenv("API_URL_SD")
HF_KEY = os.getenv("HF_KEY")
headers = {"Authorization": HF_KEY}

IMAGE_DIR = "/root/AIVideos/data/images"

def generate_image_hf(data):
    # Iterate over each scene in the storyboard
    for scene in data:
        scene_id = scene["id"]
        for image in scene["images"]:
            id = image["id"]
            prompt = image["image"]

            # Retry mechanism
            attempts = 0
            max_attempts = 5
            delay = 30  # Initial delay in seconds

            while attempts < max_attempts:
                # Generate the image via the OpenAI API
                print(f"Generating image for scene {scene_id}, image id {id}, attempt {attempts + 1}")
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "guidance_scale": 0,
                        "num_inference_steps": 4,
                        "width": 576,
                        "height": 1024,
                    },
                }
                
                response = requests.post(API_URL, headers=headers, json=payload)

                if response.status_code == 200:
                    # Successful request
                    image_bytes = response.content

                    # Create a filename and save the image
                    unique_id = uuid.uuid4().hex[:8]
                    generated_image_name = f"image_{scene_id}_{id}_{unique_id}.png"
                    generated_image_filepath = os.path.join(IMAGE_DIR, generated_image_name)
                    with open(generated_image_filepath, "wb") as image_file:
                        image_file.write(image_bytes)

                    # Update the JSON with the file path
                    image["file_name"] = generated_image_name
                    
                    # Introduce a 3-second inter-call delay after a successful request
                    time.sleep(3)
                    break  # Exit the retry loop on success
                
                elif response.status_code == 429:
                    # Too Many Requests; wait and retry
                    print(f"Rate limit hit for scene {scene_id}, image id {id}. Retrying in {delay} seconds...")
                    attempts += 1
                    time.sleep(delay)
                    delay *= 2  # Exponentially increase the delay
                
                else:
                    # Log other errors and break
                    print(f"Error {response.status_code} for scene {scene_id}, image id {id}: {response.text}")
                    break

            else:
                # If max_attempts are reached without success, raise an exception or handle it
                print(f"Failed to generate image for scene {scene_id}, image id {id} after {max_attempts} attempts.")
                return False  # Indicate failure for this image

    return True  # Indicate successful completion for all images
