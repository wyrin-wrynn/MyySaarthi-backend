import praw
from urllib.parse import urlparse, parse_qs

# Function to fetch Reddit post details using PRAW
def get_reddit_content(url):
    # Initialize PRAW with your Reddit app credentials
    reddit = praw.Reddit(
        client_id="hxPGqMkJ6YjcS6Km8cVNDQ",      # Replace with your client ID
        client_secret="g5D8ykQ3R8IJ1_zR2VbIBOxXBZwVcg",  # Replace with your client secret
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
            "text": submission.selftext
        }
    except Exception as e:
        return {"title": "Error", "text": f"An error occurred: {str(e)}"}

# Example usage
url = "https://www.reddit.com/r/pakistan/comments/1h7w4qq/horrified_by_the_language_used_by_a_10_year_old/"
result = get_reddit_content(url)
print(f"Title: {result['title']}\nText: {result['text']}")
