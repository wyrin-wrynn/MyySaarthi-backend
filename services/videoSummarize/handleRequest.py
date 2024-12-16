from pymongo import ReturnDocument
from bson.objectid import ObjectId
from db_utils import db_client
from datetime import datetime
from services.videoSummarize.getTranscription import get_source
from services.videoSummarize.generateSection import generate_section

# Get the database and collection from the MongoDB client
db = db_client.get_client()["saarthi"]
video_summary_collection = db["videoSummary"]



def get_content(url: str, summary_option: str, explanation_option: str):
    try:
        # Check if the document with the given URL already exists
        existing_document = video_summary_collection.find_one({"url": url})

        if existing_document:
            # If the document exists, check for the requested section and tone
            summaries = existing_document.get("summaries", {})
            if summary_option in summaries and explanation_option in summaries[summary_option]:
                # If the requested section and tone exist, return them
                print("Summary and tone already exist")
                return {
                    "status": "exists",
                    "title": existing_document["title"],
                    "body": existing_document["body"],
                    "summaries": summaries,
                }
            else:
                # Generate the missing section and tone
                print("Generating new section and tone")
                title = existing_document["title"]
                body = existing_document["body"]
                
                try:
                    generated_content = generate_section(title, body, summary_option, explanation_option)

                    # Update the document with the new section and tone
                    video_summary_collection.update_one(
                        {"url": url},
                        {
                            "$set": {
                                f"summaries.{summary_option}.{explanation_option}": generated_content,
                                "updatedAt": datetime.now(),
                            }
                        }
                    )

                    # Update the summaries object with the new content
                    summaries[summary_option] = summaries.get(summary_option, {})
                    summaries[summary_option][explanation_option] = generated_content

                    return {
                        "status": "updated",
                        "title": title,
                        "body": body,
                        "summaries": summaries,
                    }

                except Exception as e:
                    print(f"Error in generating section: {str(e)}")
                    return {
                        "status": "partial_update",
                        "title": title,
                        "body": body,
                        "error": "Failed to generate the section",
                        "summaries": summaries,
                    }

        # If the document does not exist, scrape the source
        content_response = get_source(url)
        title = content_response.get('title', '')
        body = content_response.get('body', '')

        # Prepare the document to insert into the database
        document = {
            "url": url,
            "title": title,
            "body": body,
            "summaries": {},  # Initially empty
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
        }

        # Insert the document into the collection
        video_summary_collection.insert_one(document)
        print("Document created successfully in the database")

        # Generate the initial summary for the requested section and tone
        try:
            generated_content = generate_section(title, body, summary_option, explanation_option)

            # Update the document with the generated summary
            video_summary_collection.update_one(
                {"url": url},
                {
                    "$set": {
                        f"summaries.{summary_option}.{explanation_option}": generated_content,
                        "updatedAt": datetime.now(),
                    }
                }
            )

            return {
                "status": "created_and_updated",
                "title": title,
                "body": body,
                "summaries": {
                    summary_option: {
                        explanation_option: generated_content
                    }
                },
            }

        except Exception as e:
            print(f"Error in generating section: {str(e)}")
            return {
                "status": "created_but_failed_to_generate",
                "title": title,
                "body": body,
                "error": "Failed to generate the section",
                "summaries": {},
            }

    except Exception as e:
        # Log and raise the exception for API error handling
        print(f"Error in get_content: {str(e)}")
        raise
