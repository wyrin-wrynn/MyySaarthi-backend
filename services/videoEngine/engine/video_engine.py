import time
from services.videoEngine.sourceGen import reddit, news, wiki, ytscript, generateSource, perplexity
from services.videoEngine.scriptGen import createScript, createStoryboard
from services.videoEngine.imageGen import createImage
from services.videoEngine.audioGen import createTranscription, createAudioEdge
from services.videoEngine.utils import db_utils, utils

def getSource(source, url, aspect="portrait", duration=60):
    source_handlers = {
        "Perplexity": perplexity.get_summary_from_query,
        "Reddit URL": reddit.get_content,
        "News Article URL": news.get_content,
        "Wikipedia URL": wiki.get_content,
        "YouTube URL": ytscript.get_content,
        "Generate Random Topic": generateSource.get_content
    }

    # Generate a unique filename for the project
    filename = db_utils.get_unique_filename(url)
    data = {'url': url, 'aspect': aspect, 'duration': int(duration)}

    # Start timing
    start_time = time.time()

    handler_function = source_handlers[source]
    source_data = handler_function(url)
    data['title'] = source_data['title']
    data['body'] = source_data['body']
    source_info = {'title': data['title'], 'body': data['body']}

    # Yield with cumulative time
    yield f"Got the Source - {round(time.time() - start_time, 2)} seconds"
    yield source_info
    print("Got source")
    db_utils.create_project_document(data,filename)

