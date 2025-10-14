import os
import subprocess
from datetime import timedelta
import streamlit as st
import whisper
import srt
from moviepy.video.io.VideoFileClip import VideoFileClip

# --------------------------
# Utility: Extract Audio
# --------------------------
def extract_audio(video_path, output_audio_path):
    print("Starting extraction...")
    try:
        if not os.path.exists(video_path):
            print(f"File not found: {video_path}")
            return None

        print("Loading video...")
        with VideoFileClip(video_path) as video:
            if video.audio:
                print("Extracting audio...")
                video.audio.write_audiofile(output_audio_path, codec='pcm_s16le')
                print(f"Audio saved at: {output_audio_path}")
                return output_audio_path
            else:
                print("No audio track found.")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# --------------------------
# Utility: Transcribe Audio
# --------------------------
def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

# --------------------------
# Utility: Convert to SRT
# --------------------------
def gen_srt(transcription_result):
    try:
        segments = transcription_result['segments']
        subtitles = []
        for i, seg in enumerate(segments):
            subtitle = srt.Subtitle(
                index=i + 1,
                start=timedelta(seconds=seg['start']),
                end=timedelta(seconds=seg['end']),
                content=seg['text'].strip()
            )
            subtitles.append(subtitle)
        return srt.compose(subtitles)
    except Exception as e:
        print(f"SRT generation error: {e}")
        return ""

# --------------------------
# Utility: Burn Subtitles
# --------------------------
def burn_subtitles(video_path, srt_relative_path, output_path, ffmpeg_path):
    try:
        video_full = os.path.abspath(video_path)
        output_full = os.path.abspath(output_path)

        command = f'"{ffmpeg_path}" -i "{video_full}" -vf subtitles={srt_relative_path} "{output_full}"'
        print("Running FFmpeg command:")
        print(command)

        subprocess.run(command, shell=True, check=True)
        print(f"✅ Video with burned-in captions generated: {output_full}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while burning subtitles: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# --------------------------
# Streamlit UI Setup
# --------------------------
def main():
    st.set_page_config(page_title="AI Video Caption Generator", layout="wide")
    st.title("🎬 AI-Powered Video Caption Generator")
    st.write("Generate automatic subtitles for your videos using **OpenAI Whisper** (offline).")
    
    # File uploader
    uploaded_video = st.file_uploader("🎥 Upload your video file", type=["mp4", "mov"])
    if uploaded_video:
        video_path = "video/upload.mp4"
        os.makedirs("video", exist_ok=True)
        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())
        st.video(video_path)

        if st.button("🚀 Generate Captions"):
            os.makedirs("audio", exist_ok=True)
            audio_path = "audio/sample.wav"
            st.write("🎧 Extracting audio...")
            if not extract_audio(video_path, audio_path):
                st.error("Failed to extract audio!")
                return
            
            st.write("🧠 Transcribing audio...")
            transcription_result = transcribe_audio(audio_path)
            if not transcription_result:
                st.error("Failed to transcribe audio!")
                return

            st.write("📝 Generating subtitles...")
            srt_content = gen_srt(transcription_result)
            if not srt_content:
                st.error("Failed to generate subtitles!")
                return

            os.makedirs("captions", exist_ok=True)
            srt_path = "captions/output.srt"
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)
            st.success("✅ SRT Generated Successfully!")

            ffmpeg_path = r"C:\ffmpeg-2025-10-12-git-0bc54cddb1-essentials_build\bin\ffmpeg.exe"
            st.write("🔥 Burning subtitles onto video...")
            if burn_subtitles(video_path, srt_path, "video/output.mp4", ffmpeg_path):
                st.success("🎥 Video ready with subtitles!")
                st.video("video/output.mp4")
            else:
                st.error("Failed to burn subtitles! Check console logs for details.")


if __name__ == "__main__":
    main()