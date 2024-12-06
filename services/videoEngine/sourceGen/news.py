from newspaper import Article

def get_content(url):
    try:
        # Initialize and download the article
        article = Article(url)
        article.download()
        article.parse()

        # Extract required information
        info = {
            "title": article.title,
            "body": article.text,
        }
        return info

    except Exception as e:
        # Return error information if something goes wrong
        return {"error": f"An error occurred: {str(e)}"}
