import json
import re
import string
import unicodedata
from fuzzywuzzy import fuzz
from num2words import num2words

def merge_scene_data(json1, json2):
    json3 = {}
    for scene in json1:
        scene_id = scene["id"]
        json3[scene_id] = {
            "id": scene_id,
            "narration": scene["narration"],
            "tone": scene["tone"],
            "theme": scene["theme"],
            "emotions": scene["emotions"],
            "colorScheme": scene["colorScheme"],
            "images": []
        }

    for image_entry in json2:
        scene_id = image_entry["scene_id"]
        if scene_id in json3:
            json3[scene_id]["images"].append({
                "id": image_entry["id"],
                "image": image_entry["image"],
                "narration_chunk": image_entry["narration_chunk"]
            })

    return list(json3.values())

def merge_scene_data(json1, json2):
    json3 = {}
    for scene in json1:
        scene_id = scene["id"]
        json3[scene_id] = {
            "id": scene_id,
            "narration": scene["narration"],
            "tone": scene["tone"],
            "theme": scene["theme"],
            "emotions": scene["emotions"],
            "colorScheme": scene["colorScheme"],
            "images": []
        }

    for image_entry in json2:
        scene_id = image_entry["scene_id"]
        if scene_id in json3:
            json3[scene_id]["images"].append({
                "id": image_entry["id"],
                "image": image_entry["image"],
                "narration_chunk": image_entry["narration_chunk"]
            })

    return list(json3.values())

def normalize(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-')
    words = text.split()
    normalized_words = []
    for word in words:
        try:
            numeric_form = int(word)
            word = num2words(numeric_form)
        except ValueError:
            pass
        normalized_words.append(word)
    text = ' '.join(normalized_words)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower().strip(string.punctuation)
    return text

def process_video_json(data):
    def adaptive_window_phrase_matching(transcription_words, narration_chunk):
        # Tokenize and normalize the narration chunk
        narration_tokens = normalize(narration_chunk).split()
        n = len(narration_tokens)
        best_score = 0
        best_match = None
        start_time, end_time = None, None

        # Sliding window with adaptive size
        for i in range(len(transcription_words) - n + 1):
            # Take a window from the transcription
            transcription_window = transcription_words[i:i + n]
            transcription_window_text = ' '.join([word_obj["word"] for word_obj in transcription_window])
            
            # Calculate similarity score with the narration chunk
            score = fuzz.token_set_ratio(transcription_window_text, narration_chunk)

            # If the score is higher than previous best, update best match
            if score > best_score:
                best_score = score
                best_match = transcription_window
                start_time = transcription_window[0]["previous_end"]
                end_time = transcription_window[-1]["end"]
        
        # Return best match if score is above a threshold
        if best_score > 70:  # Confidence threshold for a match
            return start_time, end_time
        else:
            return None, None

    # Process each scene
    for scene in data:
        previous_end = 0.0
        
        # Prepare transcription words with timestamps
        for word_obj in scene["transcription"]:
            word_obj["word"] = normalize(word_obj["word"])
            word_obj["previous_end"] = previous_end
            duration = word_obj["end"] - previous_end
            word_obj["duration"] = round(duration, 2)
            previous_end = word_obj["end"]

        transcription_words = scene["transcription"]
        
        for image in scene["images"]:
            narration_chunk_normalized = normalize(image["narration_chunk"])
            
            # Apply adaptive window phrase matching to find start and end times
            start_time, end_time = adaptive_window_phrase_matching(transcription_words, narration_chunk_normalized)

            if start_time is not None and end_time is not None:
                image["start"] = start_time
                image["end"] = end_time
                image["duration"] = round(end_time - start_time, 2)
            else:
                print(f"Warning: Could not find matching sequence for image {image['id']} in scene {scene['id']}")

    return data