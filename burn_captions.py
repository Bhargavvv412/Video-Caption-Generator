import subprocess
import os

def burn_subtitles(video_path,srt_relative_path,output_path,ffmpeg_path):
    video_full = os.path.abspath(video_path)
    output_full = os.path.abspath(output_path)

    command = f'"{ffmpeg_path}" -i "{video_full}" -vf "subtitles={srt_relative_path}" "{output_full}"'

    print("command running")

    print(command)

    try:
        subprocess.run(command,shell=True,check=True)
        print(f"Video burned-in caption generated: {output_full}")  

    except subprocess.CalledProcessError as e:
        print(f"Error {e}")

if __name__ == "__main__":
    ffmpeg_path = r"C:\ffmpeg-2025-10-12-git-0bc54cddb1-essentials_build\bin\ffmpeg.exe"

    video_file = "video/sample.mp4"
    srt_relative_path = "captions/output.srt"
    output_path = "video/output.mp4"

    burn_subtitles(video_file,srt_relative_path,output_path,ffmpeg_path)