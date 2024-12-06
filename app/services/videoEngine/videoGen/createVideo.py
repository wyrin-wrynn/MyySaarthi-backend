import json
import os
import uuid

from videoGen.ken_burns import create_smooth_pan_zoom_video
from videoGen.concat_tools import concat_clips, concat_with_fade
from videoGen.subtitles import add_subtitles_to_video


def create_video(data):
    # Set up directory to save temp files
    clips_dir = "/root/AIVideos/data/clips/"
    image_dir = "/root/AIVideos/data/images/"
    video_dir = "/root/AIVideos/data/videos/"

    # Debug: Start of process
    print("Starting video creation process")

    # Create Ken Burns video clips
    for scene in data:
        scene_id = scene["id"]
        for image in scene["images"]:
            image_id = image["id"]
            image_path = os.path.join(image_dir, image["file_name"])
            duration = image["duration"]
            unique_id = uuid.uuid4().hex[:8]
            generated_clip_name = f"clips_{scene_id}_{image_id}_{unique_id}.mp4"
            generated_clip_filepath = os.path.join(clips_dir, generated_clip_name)

            # Attempt to create Ken Burns effect video
            try:
                image["clip"] = create_smooth_pan_zoom_video(image_path, generated_clip_filepath, duration)
            except Exception as e:
                print(f"Error creating Ken Burns video for Image ID {image_id}: {e}")

    # Join those video clips to create scene video and add subtitles
    for scene in data:
        scene_id = scene["id"]
        
        clips = []
        for image in scene["images"]:
            clip = image.get("clip")
            if clip:
                clips.append(clip)
            else:
                print(f"Warning: No clip found for Image ID {image['id']} in Scene ID {scene_id}")

        # Concatenate scene clips
        unique_id = uuid.uuid4().hex[:8]
        generated_scene_name = f"scene_clips_{scene_id}_{unique_id}.mp4"
        generated_scene_filepath = os.path.join(clips_dir, generated_scene_name)

        try:
            scene["scene_clip"] = concat_clips(clips, generated_scene_filepath)
        except Exception as e:
            print(f"Error concatenating clips for Scene ID {scene_id}: {e}")

        # Concatenate scene clips
        unique_id = uuid.uuid4().hex[:8]
        generated_scene_name_sub_titles = f"scene_subtitles_{scene_id}_{unique_id}.mp4"
        generated_scene_filepath_sub_titles = os.path.join(clips_dir, generated_scene_name_sub_titles)


        # Add subtitles
        subtitles = scene.get("transcription", "")
        audio_file = scene.get("audio_file", "")
        if subtitles and audio_file:
            try:
                scene["scene_clip"] = add_subtitles_to_video(
                    subtitles, generated_scene_filepath, audio_file, generated_scene_filepath_sub_titles
                )
            except Exception as e:
                print(f"Error adding subtitles to Scene ID {scene_id}: {e}")

    # Combine scene videos to create final video
    unique_id = uuid.uuid4().hex[:8]
    generated_video_name = f"videos_{unique_id}.mp4"
    generated_video_filepath = os.path.join(video_dir, generated_video_name)
    video_paths = [scene["scene_clip"] for scene in data if scene.get("scene_clip")]


    # Debug: Final video concatenation
    try:
        concat_with_fade(video_paths, generated_video_filepath)
        print(f"Final video created at {generated_video_filepath}")
    except Exception as e:
        print(f"Error in final video concatenation: {e}")

    return generated_video_filepath