from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def extract_audio(video_path, output_audio_path):
    print("Starting extraction...")  # debug point
    try:
        if not os.path.exists(video_path):
            print(f"File not found: {video_path}")
            return

        print("Loading video...")
        with VideoFileClip(video_path) as video:
            if video.audio:
                print("Extracting audio...")
                video.audio.write_audiofile(output_audio_path, codec='pcm_s16le')
                print(f"Audio saved at: {output_audio_path}")
            else:
                print("No audio track found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_file = "video/sample.mp4"
    audio_output = "audio/sample.wav"

    os.makedirs(os.path.dirname(audio_output), exist_ok=True)
    extract_audio(video_file, audio_output)
