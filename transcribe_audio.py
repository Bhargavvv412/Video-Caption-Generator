import whisper

def transcribe(audio_path):
    model = whisper.load_model("base")
    result  = model.transcribe(audio_path)

    #Print transcript
    print("\n Transctiption Result")
    print(result['text'])

    return result

if __name__ == "__main__":
    audio_file = "audio/sample.wav"
    transcribe(audio_file)
    