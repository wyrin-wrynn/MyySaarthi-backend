import cv2
import numpy as np
from PIL import Image
import math

def create_smooth_pan_zoom_video(image_path, output_video_path, duration, zoom_factor=0.9, fps=24, direction="right", easing="ease-in-out", upscale_factor=2, pan_percent=0.1, mode="zoom-in"):
    """Main function to create a zoom-in or zoom-pan-in video with panning direction control."""
    image = Image.open(image_path)
    original_width, original_height = image.size
    upscale_width, upscale_height = original_width * upscale_factor, original_height * upscale_factor
    image = image.resize((upscale_width, upscale_height), Image.LANCZOS)

    num_frames = int(fps * duration)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (original_width, original_height))

    if mode == "zoom-in":
        zoom_in_mode(image, zoom_factor, num_frames, video_writer, original_width, original_height, upscale_width, upscale_height, easing)
    elif mode == "zoom-pan-in":
        zoom_pan_in_mode(image, zoom_factor, num_frames, pan_percent, direction, video_writer, original_width, original_height, upscale_width, upscale_height, easing)

    video_writer.release()
    print(f"Video saved as {output_video_path}")
    return output_video_path

def zoom_in_mode(image, zoom_factor, num_frames, video_writer, original_width, original_height, upscale_width, upscale_height, easing):
    """Zoom-in mode only."""
    zoom_width, zoom_height = upscale_width, upscale_height

    for i in range(num_frames):
        progress = apply_easing(i, num_frames, easing)
        zoom_width, zoom_height, _, _ = get_zoom_dimensions(
            upscale_width, upscale_height, zoom_width, zoom_height, 0, 0, zoom_factor, progress, "in"
        )
        left, top, right, bottom = calculate_crop_area(0, 0, zoom_width, zoom_height, upscale_width, upscale_height)
        process_frame(image, left, top, right, bottom, original_width, original_height, video_writer)

def zoom_pan_in_mode(image, zoom_factor, num_frames, pan_percent, direction, video_writer, original_width, original_height, upscale_width, upscale_height, easing):
    """Zoom-in with pan in a specified direction."""
    zoom_width, zoom_height = upscale_width, upscale_height

    for i in range(num_frames):
        progress = apply_easing(i, num_frames, easing)
        zoom_width, zoom_height, _, _ = get_zoom_dimensions(
            upscale_width, upscale_height, zoom_width, zoom_height, 0, 0, zoom_factor, progress, "in"
        )
        pan_offset_x, pan_offset_y = get_pan_offsets(progress, direction, zoom_width, zoom_height, pan_percent)
        left, top, right, bottom = calculate_crop_area(pan_offset_x, pan_offset_y, zoom_width, zoom_height, upscale_width, upscale_height)
        process_frame(image, left, top, right, bottom, original_width, original_height, video_writer)

def apply_easing(frame_index, num_frames, easing):
    """Apply easing based on the chosen type."""
    t = frame_index / (num_frames - 1)
    if easing == "ease-in":
        return t * t
    elif easing == "ease-out":
        return 1 - (1 - t) * (1 - t)
    elif easing == "ease-in-out":
        return (1 - math.cos(t * math.pi)) / 2
    else:
        return t

def get_pan_offsets(progress, direction, width, height, pan_percent):
    """Calculate pan offsets based on direction and current zoom dimensions."""
    max_offset_x = width * pan_percent
    max_offset_y = height * pan_percent
    pan_offset_x = int(max_offset_x * progress) if "right" in direction else -int(max_offset_x * progress)
    pan_offset_y = int(max_offset_y * progress) if "bottom" in direction else -int(max_offset_y * progress)
    return pan_offset_x, pan_offset_y

def get_zoom_dimensions(original_width, original_height, zoom_width, zoom_height, accumulated_width, accumulated_height, zoom_factor, progress, zoom_direction):
    """Calculate zoom dimensions for zoom-in."""
    target_zoom_width = original_width * (zoom_factor ** progress)
    target_zoom_height = original_height * (zoom_factor ** progress)
    accumulated_width += target_zoom_width - zoom_width
    accumulated_height += target_zoom_height - zoom_height
    if abs(accumulated_width) >= 1.0:
        zoom_width += int(accumulated_width)
        accumulated_width -= int(accumulated_width)
    if abs(accumulated_height) >= 1.0:
        zoom_height += int(accumulated_height)
        accumulated_height -= int(accumulated_height)
    return zoom_width, zoom_height, accumulated_width, accumulated_height

def calculate_crop_area(pan_offset_x, pan_offset_y, zoom_width, zoom_height, original_width, original_height):
    """Calculate cropping area based on zoom and pan offsets."""
    int_zoom_width = int(round(zoom_width))
    int_zoom_height = int(round(zoom_height))
    left = pan_offset_x + (original_width - int_zoom_width) // 2
    top = pan_offset_y + (original_height - int_zoom_height) // 2
    right = left + int_zoom_width
    bottom = top + int_zoom_height
    left = max(0, min(left, original_width - int_zoom_width))
    top = max(0, min(top, original_height - int_zoom_height))
    right = min(original_width, right)
    bottom = min(original_height, bottom)
    return left, top, right, bottom

def process_frame(image, left, top, right, bottom, output_width, output_height, video_writer):
    """Crop, resize, and write the current frame to the video."""
    cropped_image = image.crop((left, top, right, bottom))
    resized_image = cropped_image.resize((output_width, output_height), Image.LANCZOS)
    frame = cv2.cvtColor(np.array(resized_image), cv2.COLOR_RGB2BGR)
    video_writer.write(frame)

