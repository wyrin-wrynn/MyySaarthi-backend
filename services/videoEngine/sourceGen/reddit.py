import praw
from urllib.parse import urlparse, parse_qs
import os

# Function to fetch Reddit post details using PRAW
def get_content(url):
    # Initialize PRAW with your Reddit app credentials
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_ID"),      # Replace with your client ID
        client_secret=os.getenv("REDDIT_SECRET"),  # Replace with your client secret
        user_agent="saarthi"    # Replace with your user agent
    )
    
    # Extract post ID from the URL
    try:
        parsed_url = urlparse(url)
        post_id = parsed_url.path.split("/")[4]  # Extract the post ID from URL
        
        # Fetch submission by ID
        submission = reddit.submission(id=post_id)
        
        # Return title and text
        return {
            "title": submission.title,
            "body": submission.selftext
        }
    except Exception as e:
        return {"title": "Error", "body": f"An error occurred: {str(e)}"}