import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 0.5)


def speak(text):
    engine.say(text)
    engine.runAndWait()