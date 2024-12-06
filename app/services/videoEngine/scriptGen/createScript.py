from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from app.services.videoEngine.scriptGen import prompts
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def generate_script(title: str, body: str):
    class Scene(BaseModel):
        id: str
        narration: str
        tone: str
        theme: str
        emotions: str
        visuals: str
        colorScheme: str

    class Storyboard(BaseModel):
        storyboard: List[Scene]
    
    client = OpenAI(api_key=api_key)

    # Construct the prompt to provide the context for storyboard generation
    prompt = prompts.generate_script_prompt

    # Form the user's message
    user_message = f"Title: {title}\nBody: {body}"

    try:
        # Make a call to OpenAI's API with structured response parsing
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",  # Adjust model name as required
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            response_format=Storyboard,  # Use Storyboard model for structured parsing
        )

        # Extract the parsed storyboard from the response
        storyboard = completion.choices[0].message.parsed.storyboard
        script = []
        for scene in storyboard:
            temp_scene = {}
            temp_scene["id"] = scene.id
            temp_scene["narration"]=scene.narration
            temp_scene["tone"]=scene.tone
            temp_scene["theme"]=scene.theme
            temp_scene["emotions"]=scene.emotions
            temp_scene["colorScheme"]=scene.colorScheme

            script.append(temp_scene)

        print("Storyboard is created")
        return script

    except Exception as e:
        return {"error": str(e)}
    

def generate_general_script(title: str, body: str, duration: int):
    class Scene(BaseModel):
        id: int
        narration: str

    class Script(BaseModel):
        scenes: List[Scene]
        tone: str
        theme: str
        emotions: str
        colorScheme: str
        title: str
        description: str
    
    client = OpenAI(api_key=api_key)

    # Construct the prompt to provide the context for storyboard generation
    prompt = prompts.generate_general_script

    # Form the user's message
    user_message = f"Title: {title}\n Body: {body}\n Duration: {duration} minutes"

    try:
        # Make a call to OpenAI's API with structured response parsing
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",  # Adjust model name as required
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            response_format=Script,  # Use Storyboard model for structured parsing
        )

        # Extract the parsed storyboard from the response
        script = completion.choices[0].message.parsed
        temp_script = {}
        temp_script["title"]=script.title
        print("title is read")
        temp_script["tone"]=script.tone
        temp_script["theme"]=script.theme
        temp_script["emotions"]=script.emotions
        temp_script["colorScheme"]=script.colorScheme
        temp_script["description"]=script.description
        temp_script["scnees"] = []
        
        for scene in script['scenes']:
            temp_scene={}
            temp_scene["id"]=scene.id
            temp_scene["narration"]=scene.narration
            temp_script["scnees"].append(temp_scene)

        

        print("Script is created")
        return temp_script

    except Exception as e:
        return {"error": str(e)}