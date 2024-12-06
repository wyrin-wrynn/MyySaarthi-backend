import time
from sourceGen import reddit, news, wiki, ytscript, generateSource
from scriptGen import createScript, createStoryboard
from imageGen import createImage
from audioGen import createTranscription, createAudioEdge
from utils import db_utils, utils
from videoGen import createVideo


def short_engine(source, url):
    source_handlers = {
        "Reddit URL": reddit.get_content,
        "News Article URL": news.get_content,
        "Wikipedia URL": wiki.get_content,
        "YouTube URL": ytscript.get_content,
        "Generate Random Topic": generateSource.get_content
    }

    filename = db_utils.get_unique_filename(url)

    data = {}
    data['url'] = url

    # Start timing
    start_time = time.time()

    # Step 1: Getting source information
    handler_function = source_handlers[source]
    source_data = handler_function(url)
    data['title'] = source_data['title']
    data['body'] = source_data['body']
    source_info = {'title': data['title'], 'body': data['body']}
    
    # Yield with cumulative time
    yield f"Got the Source - {round(time.time() - start_time, 2)} seconds"
    yield source_info
    print("Got source")
    db_utils.create_project_file(data,filename)
    
    # Step 2: Generate script
    data['script'] = createScript.generate_script(data['title'], data['body'])
    yield f"Script is done - {round(time.time() - start_time, 2)} seconds"
    db_utils.create_project_file(data,filename)
    print("Generated SCript")
    
    # Step 3: Generate storyboard
    data['storyBoard'] = createStoryboard.generate_storyboard(data['script'])
    yield f"Got StoryBoard - {round(time.time() - start_time, 2)} seconds"
    db_utils.create_project_file(data,filename)
    print("Generated Storyboard")

    # Step 4: Create movie JSON
    data['videoJson'] = utils.merge_scene_data(data['script'], data['storyBoard'])
    yield f"Movie Json created - {round(time.time() - start_time, 2)} seconds"
    db_utils.create_project_file(data,filename)
    print("Generated Json")

    # Step 5: Generate audio clips for narrations
    createAudioEdge.create_audio_for_narrations(data['videoJson'])
    yield f"Audio Clips created - {round(time.time() - start_time, 2)} seconds"
    db_utils.create_project_file(data,filename)
    print("Created Audio")

    # Step 6: Generate transcription
    createTranscription.createTranscription(data['videoJson'])
    yield f"Transcription created - {round(time.time() - start_time, 2)} seconds"
    db_utils.create_project_file(data,filename)
    print("Created trasncription")

    # Step 7: Create video compile json
    utils.process_video_json(data['videoJson'])
    yield f"Durations and Tags created - {round(time.time() - start_time, 2)} seconds"
    db_utils.create_project_file(data,filename)
    print("created movie json")

    # Step 8: Generate Images
    createImage.generate_image_hf(data['videoJson'])
    yield f"Images created - {round(time.time() - start_time, 2)} seconds"
    db_utils.create_project_file(data,filename)
    print("Created images")

    # Step 9: Generate Video
    final_video = createVideo.create_video(data['videoJson'])
    yield f"Video engine done - {round(time.time() - start_time, 2)} seconds"
    data["final_video"] = final_video
    db_utils.create_project_file(data,filename)
    print("Created videos")

    # Step 10: Save project file
    db_utils.create_project_file(data,filename)
    yield f"File created - {filename} - {round(time.time() - start_time, 2)} seconds"
    print("File saved")

    return data
