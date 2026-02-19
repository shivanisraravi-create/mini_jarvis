import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import webbrowser
import tempfile
import scipy.io.wavfile as wav

TRIGGER_WORD_1 = "jarvis"
TRIGGER_WORD_2 = "up"

SAMPLE_RATE = 16000
DURATION = 5  # seconds to listen

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def record_audio():
    print("Listening...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE),
                       samplerate=SAMPLE_RATE,
                       channels=1,
                       dtype='int16')
    sd.wait()
    return recording

def recognize_speech(audio_data):
    recognizer = sr.Recognizer()

    # Save temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        wav.write(temp_audio.name, SAMPLE_RATE, audio_data)

        with sr.AudioFile(temp_audio.name) as source:
            audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        print("Internet issue.")
        return ""

def main():
    audio_data = record_audio()
    spoken_text = recognize_speech(audio_data)

    if TRIGGER_WORD_1 in spoken_text and TRIGGER_WORD_2 in spoken_text:
        speak("For you, always.")
        webbrowser.open("https://chatgpt.com")

if __name__ == "__main__":
    main()
