import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "use_your-own-newsapi-key"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('temp.mp3')

def aiProcess(command):
    client = OpenAI(api_key="use_your-own-openai-api-key",
)
    completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named JARVIS. You are designed to assist users with various tasks, including answering questions, providing information, and performing actions based on user commands, like Alexa or Siri or Google Assistant.Give short reponces please."},
        {"role": "user", "content": command}
  ]
)

    return (completion.choices[0].message.content)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = music_library.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            #  Parse the JSON response
            data = r.json()

            #  Extract the articles
            articles = data.get('articles', [])

            # print the headlines
            for article in articles:
                speak(article['title'])

        else:
            # let the OpenAI handle the request..
            output = aiProcess(c)
            speak(output)

if __name__ == "__main__":
    speak("Initializing JARVIS...")
    while True:
        # Listen for the wake word "JARVIS"
        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using Google
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listining...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("Ya")
                #  Listen for the command after the wake word
                with sr.Microphone() as source:
                    print("JARVIS Activated...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
