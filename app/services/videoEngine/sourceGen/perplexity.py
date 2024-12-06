import requests
import os
from .prompts import perplexity_prompt

def get_summary_from_query(user_query):
    """
    Fetch a summary of the user query using the Perplexity API.

    Args:
        user_query (str): The question or query to get a summarized response for.

    Returns:
        str: A textual summary of the response or an error message if the process fails.
    """
    # Environment variable for the token
    token = os.getenv("TOKEN")
    
    if not token:
        return "Error: Missing API token. Ensure the 'TOKEN' environment variable is set."
    
    url = "https://api.perplexity.ai/chat/completions"
    
    # System state definition
    system_state = perplexity_prompt
    
    # Payload for the request
    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [
            {
                "role": "system",
                "content": system_state
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        "max_tokens": 16000,
        "temperature": 0.7,
        "top_p": 0.9,
        "search_recency_filter": "month",
        "search_domain_filter": [
            "ndtv.com",
            "theprint.in",
            "financialexpress.com"
        ]
    }
    
    # Headers for the request
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    try:
        # Send the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            return f"Error: API request failed with status code {response.status_code}. Response: {response.text}"
        
        # Parse the JSON response
        data = response.json()
        
        # Extract and return the summary
        summary = data['choices'][0]['message']['content']
        return {'title': user_query, 'body': summary}
    
    except KeyError as e:
        return f"KeyError: Missing key {e} in the response. Here is the raw response for debugging: {response.json()}"
    except Exception as ex:
        return f"Error: An unexpected error occurred: {str(ex)}"
