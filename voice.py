import time
import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()
r.pause_threshold = 0.8  # allow short pauses

def speak(text):
    # print("SPEAKING:", repr(text))
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def calibrate():
    # speak("Calibrating microphone. Please be quiet.")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1.0)
    # speak("Ready.")

def listen(timeout=10, phrase_time_limit=4):
    try:
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return r.recognize_google(audio).lower().strip()
    except sr.WaitTimeoutError:
        speak("I didn't hear anything.")
        return None
    except sr.UnknownValueError:
        speak("I couldn't understand that.")
        return None
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return None

def ask(prompt):
    speak(prompt)
    time.sleep(0.1) # Wait to listen
    return listen()
