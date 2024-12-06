import os
from dotenv import load_dotenv
from openai import OpenAI
from .prompts import generate_prompt
from pydantic import BaseModel, Field


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

class Story(BaseModel):
    title: str
    body: str

def get_content(topic="No topic"):
    client = OpenAI(api_key=api_key)
    prompt = generate_prompt
    try:
        # Make a call to OpenAI's API with structured response parsing
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",  # Adjust model name as required
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ],
            response_format=Story,  # Use Storyboard model for structured parsing
        )

        # Extract the parsed storyboard from the response
        title = completion.choices[0].message.parsed.title
        body = completion.choices[0].message.parsed.body
        script = {'title': title, 'body':body}
        
        print("Story is created")
        return script

    except Exception as e:
        return {"error": str(e)}