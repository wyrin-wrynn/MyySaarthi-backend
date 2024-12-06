from moviepy.editor import TextClip, VideoFileClip, AudioFileClip, CompositeVideoClip

def add_subtitles_to_video(subtitles_data, video_file, audio_file, output_file):
    # Load the video and audio files
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    # Adjust subtitles to prevent overlaps
    def adjust_subtitles(subtitles):
        adjusted_subtitles = []
        for i, subtitle in enumerate(subtitles):
            if i == 0:
                subtitle["duration"] = subtitle["end"] - subtitle["start"]
            else:
                subtitle["start"] = max(subtitle["previous_end"], adjusted_subtitles[-1]["end"])
                subtitle["duration"] = subtitle["end"] - subtitle["start"]
            
            subtitle["end"] = subtitle["start"] + subtitle["duration"]
            adjusted_subtitles.append(subtitle)
        return adjusted_subtitles

    subtitles_data = adjust_subtitles(subtitles_data)

    # Function to create a triplet clip with highlighted active word
    def create_triplet_clip(words, active_idx, duration):
        text_clips = []
        normal_fontsize, active_fontsize = 30, 40
        normal_color, active_color = "black", "yellow"
        bg_color = "white"
        
        for i, word in enumerate(words):
            if i == active_idx:
            # Convert word to uppercase and use Montserrat Bold
                text_clip = TextClip(word.upper(), fontsize=active_fontsize, color=active_color, bg_color=bg_color, font="Montserrat-Bold").set_duration(duration)
            else:
                text_clip = TextClip(word.upper(), fontsize=normal_fontsize, color=normal_color, font="Montserrat-Bold").set_duration(duration)
            text_clips.append(text_clip)

        # Adjust positioning based on the number of words
        if len(text_clips) == 3:
            start_x = (video.w - sum(clip.w for clip in text_clips) - 20) // 2
        elif len(text_clips) == 2:
            start_x = (video.w - sum(clip.w for clip in text_clips) - 10) // 2
        else:
            start_x = (video.w - text_clips[0].w) // 2

        for i, clip in enumerate(text_clips):
            offset_x = start_x + sum(c.w + 10 for c in text_clips[:i])
            text_clips[i] = clip.set_position((offset_x, "center"))

        return CompositeVideoClip(text_clips, size=video.size).set_duration(duration)

    # Generate triplet clips based on subtitle data
    triplet_clips = []
    for i in range(0, len(subtitles_data), 3):
        triplet_words = [subtitles_data[j]["word"] for j in range(i, min(i + 3, len(subtitles_data)))]
        
        for active_word_idx in range(len(triplet_words)):
            duration = subtitles_data[i + active_word_idx]["duration"]
            start_time = subtitles_data[i + active_word_idx]["start"]

            triplet_clip = create_triplet_clip(triplet_words, active_word_idx, duration)
            triplet_clip = triplet_clip.set_start(start_time)
            triplet_clips.append(triplet_clip)

    # Concatenate triplet clips and overlay onto the main video
    triplet_sequence = CompositeVideoClip(triplet_clips, size=video.size)

    final_video = CompositeVideoClip([video, triplet_sequence]).set_audio(audio)
    final_video.write_videofile(output_file, fps=24)
    return output_file