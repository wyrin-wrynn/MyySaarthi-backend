import wikipediaapi

def get_content(url, full_text=False):
    # Extract page name from the URL
    page_name = url.split("/wiki/")[-1]
    
    # Initialize Wikipedia API with specified language and user-agent
    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent='MyProjectName (contact: myemail@example.com)', 
        language='en'
    )

    # Fetch the page
    page = wiki_wiki.page(page_name)

    if not page.exists():
        return {"error": "The Wikipedia page does not exist."}

    # Extract title
    title = page.title

    # Choose between full text and summary
    content = page.text if full_text else page.summary

    # Clean up the text for readability
    cleaned_content = content.encode("utf-8").decode("unicode_escape").replace("\n\n", "\n").replace("\n", " ").strip()

    # Return the result as a dictionary
    return {"title": title, "body": cleaned_content}

# Example usage
#url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
#wiki_info_summary = extract_wiki_info(url, full_text=False)

#wiki_info_full = extract_wiki_info(url, full_text=True)
