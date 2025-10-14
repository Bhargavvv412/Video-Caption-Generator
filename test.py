import whisper

model = whisper.load_model("base")  # or "small" / "medium" for more accuracy
result = model.transcribe("audio/sample.wav")

print("📝 Transcription:")
print(result["text"])
