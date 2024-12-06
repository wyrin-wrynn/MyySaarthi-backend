from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout

def concat_clips(clip_paths, output_path):
    print("clips path: ", clip_paths)

    # Load each clip from the provided paths
    clips = [VideoFileClip(path) for path in clip_paths]
    
    # Concatenate all clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Write the final video file to the specified output path
    final_clip.write_videofile(output_path, codec="libx264")
    
    # Close all clips to release resources
    for clip in clips:
        clip.close()
    final_clip.close()
    
    return output_path




def concat_with_fade(file_paths, output_path):
    # Load video clips and apply fade effects\
    print(file_paths)
    clips = []
    for i, path in enumerate(file_paths):
        clip = VideoFileClip(path)
        
        # Apply fade out on all but the last clip
        if i < len(file_paths) - 1:
            clip = fadeout(clip, duration=0.5)
        
        # Apply fade in on all but the first clip
        if i > 0:
            clip = fadein(clip, duration=0.5)
        
        clips.append(clip)
    
    # Concatenate the clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Write the output to the specified path
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
