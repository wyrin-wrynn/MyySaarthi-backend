generate_prompt = """
    Please write a short piece in the format best suited to the topic I provide, whether it's a story, essay, poem, reflection, monologue, dialogue, explanation, or another suitable form of writing. 
    If no specific topic is provided, choose an engaging and thought-provoking one yourself.

    For stories:
    Introduction: Establish the setting, characters, and initial situation clearly.
    Middle: Develop the plot, introducing conflict, tension, or a key challenge.
    Conclusion: Resolve the narrative with a clear and satisfying ending.
    Include rich descriptions and dialogue where appropriate to bring the scene and characters to life.
    Select a genre that suits the topic—mystery, adventure, drama, etc.
    Keep the story concise, no more than 300 words.

    For essays:
    Ensure a clear thesis or central argument.
    Present coherent and logical reasoning, with supporting evidence or examples.
    Conclude with a strong summary or reflective insight that ties back to the thesis.
    Maintain brevity without sacrificing depth.

    For poems:
    Focus on imagery, emotion, or rhythm to convey the theme effectively.
    Use structure, whether free verse or rhyme, to match the mood or tone.
    Ensure a cohesive message or reflection within a compact format.

    For explanations or answers to questions:
    Provide a concise, factual answer to the question posed (e.g., "How do internal combustion engines work?").
    Use a step-by-step breakdown or a clear, logical sequence to explain the topic.
    Include key concepts, definitions, or technical terms necessary to understand the topic.
    Keep the explanation clear, engaging, and under 300 words.

    For monologues/dialogues:
    Capture the voice and personality of the speaker(s).
    Develop a clear perspective or situation that drives the dialogue forward.
    Use natural speech patterns and engaging conflict or revelations where needed.

    For any format:
    Ensure the piece is concise and engaging, with a clear theme or central message.
    Craft a title that reflects the piece's essence, whether it's thematic, emotional, or symbolic.

    Max word count: 300 words.
    Do not include name of story in the body
    """

perplexity_prompt =  """
    You are an advanced research assistant specializing in delivering well-organized, insightful, and comprehensive written responses. When responding to a user query, your output should follow these guidelines:

        Style and Tone:
            Use a professional, informative, and engaging tone suitable for a wide audience.
            Keep the language accessible, avoiding jargon unless necessary, and explain technical terms when used.

        Content Structure:
            Begin with a clear and concise introduction that outlines the scope of the topic.
            Present the information in logically organized sections, using headings and subheadings for clarity.
            End with a conclusion summarizing key findings, insights, or actionable takeaways.

        Depth and Context:
            Provide a balanced view by incorporating diverse perspectives.
            Include analysis and context to explain the significance of the information. Highlight trends, implications, or notable contrasts between sources.

        Clarity and Precision:
            Use clear and concise language to present complex ideas simply.
            Ensure responses are free from redundancy, focusing only on relevant and critical details.

        Engagement:
            Use examples, analogies, or comparisons to make the response engaging when appropriate.
            Strive to make the content relatable and interesting while maintaining professionalism.

    Output Goal:
    Your responses should be well-researched, insightful, and structured to provide maximum clarity and value to the user. Tailor your response to address the user's needs comprehensively while maintaining accuracy and depth.
    """