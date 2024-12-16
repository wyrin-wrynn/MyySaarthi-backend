from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from services.videoSummarize import prompts

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def generate_section(title: str, body: str, section: str, tone: str) -> str:
    """
    Generates a summary for a given section and tone using the LLM.

    Args:
        title (str): Title of the video.
        body (str): Description or body of the video.
        section (str): The type of summary or explanation to generate.
        tone (str): The tone to use for the summary.

    Returns:
        str: Generated content for the specified section and tone.
    """
    client = OpenAI(api_key=api_key)

    print("Generating section: ", section, " ", tone)

    # Select the appropriate prompt based on section and tone
    section_prompt = prompts.section_prompts.get(section, "Provide a detailed explanation.")
    tone_prompt = prompts.tone_prompts.get(tone, "Use a professional tone.")

    # Construct the system prompt
    system_prompt = f"{section_prompt}\n\n{tone_prompt}"

    # Form the user's message
    user_message = f"Title: {title}\nBody: {body}"

    # Make a call to OpenAI's API
    completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Replace with your model of choice
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
    print(completion)
    # Extract and return the generated content
    content = completion.choices[0].message.content
    print("---------------")
    print(content)
    return content