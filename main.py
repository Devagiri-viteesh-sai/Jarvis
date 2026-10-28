import os 
import time 
import subprocess
import json
import wolframalpha
import requests
import webbrowser
import wikipedia
import datetime
import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import tempfile
print('LOADING YOUR A.I PERSONAL ASSISTANT JARVIS')
pygame.mixer.init()

async def speak_async(text):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        filename = f.name

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-PrabhatNeural",
        rate="-5%"
    )
    await communicate.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)
    pygame.mixer.music.unload()
    os.remove(filename)
def speak(text):
    asyncio.run(speak_async(text))


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("hello, good morning Mr. Viteesh")
        print("hello, good morning Mr. Viteesh")
    elif hour >= 12 and hour <=18:
        speak("hello, good morning Mr. Viteesh")
        print("hello, good morning Mr. Viteesh")
    else:
        speak("Its already the night time better go to sleep")
        print("Its already the night time better go to sleep")
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I AM LISTENING...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")
        except Exception as e:   # fixed typo here
            speak("Pardon me, please say that again")
            return "None"
        
        return statement
speak('LOADING YOU PERSONAL A.I ASSISTANT JARVIS')
wishMe()
if __name__ == "__main__":

    speak("JARVIS Activated")

    while True:

        speak("How can I help you?")
        statement = takeCommand().lower()

        if not statement:
            continue

        # Exit
        if ("good bye" in statement or
            "ok bye" in statement or
            "stop" in statement or
            "exit" in statement):

            speak("Your personal AI assistant JARVIS is shutting down. Goodbye!")
            print("Your personal AI assistant JARVIS is shutting down. Goodbye!")
            break

        # Wikipedia
        elif "wikipedia" in statement:

            try:
                speak("Searching Wikipedia")

                query = statement.replace("wikipedia", "")

                results = wikipedia.summary(query, sentences=3)

                print(results)
                speak(results)

            except Exception as e:

                print(e)
                speak("Sorry, I could not find information on Wikipedia.")

        # YouTube
        elif "open youtube" in statement:

            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Opening YouTube")

        # Google
        elif "open google" in statement:

            webbrowser.open_new_tab("https://www.google.com")
            speak("Opening Google")

        # Gmail
        elif "open gmail" in statement:

            webbrowser.open_new_tab("https://mail.google.com")
            speak("Opening Gmail")

        # StackOverflow
        elif "open stackoverflow" in statement:

            webbrowser.open_new_tab("https://stackoverflow.com")
            speak("Opening Stack Overflow")

                # Weather
        elif "weather" in statement:

            try:
                api_key = "8ef61edcf1c576d65d836254e11ea420"

                speak("Please tell me the city name")
                city_name = takeCommand().strip()

                url = (
                    f"https://api.openweathermap.org/data/2.5/weather?q={city_name}"
                    f"&appid={api_key}&units=metric"
                )

                response = requests.get(url, timeout=10)
                data = response.json()

                print(data)

                if response.status_code == 200 and str(data.get("cod")) == "200":

                    temperature = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    pressure = data["main"]["pressure"]
                    feels_like = data["main"]["feels_like"]
                    description = data["weather"][0]["description"]

                    report = (
                        f"The weather in {city_name} is {description}. "
                        f"The temperature is {temperature} degree Celsius. "
                        f"It feels like {feels_like} degree Celsius. "
                        f"The humidity is {humidity} percent. "
                        f"The pressure is {pressure} hectopascals."
                    )

                    print(report)
                    speak(report)

                else:

                    print(data)

                    speak("Sorry, I could not find the city.")

            except requests.exceptions.RequestException:

                speak("Unable to connect to the weather service.")

            except Exception as e:

                print(e)

                speak("An error occurred while fetching the weather.")
        # Time
        elif "time" in statement:

            current_time = datetime.datetime.now().strftime("%H:%M:%S")

            print(current_time)

            speak(f"The time is {current_time}")

        # About
        elif ("who are you" in statement or
              "what can you do" in statement):

            speak(
                "I am JARVIS version one point zero. "
                "I can search Wikipedia, open websites, "
                "tell weather information, tell time, "
                "search Google and answer questions."
            )

        # Creator
        elif ("who made you" in statement or
              "who created you" in statement):

            speak("I was built by AI Robosoft")

        # News
        elif "news" in statement:

            webbrowser.open_new_tab(
                "https://timesofindia.indiatimes.com/home/headlines"
            )

            speak("Opening Times of India headlines")

        # Search
        elif "search" in statement:

            query = statement.replace("search", "").strip()

            webbrowser.open_new_tab(
                f"https://www.google.com/search?q={query}"
            )

            speak(f"Searching Google for {query}")

        # Ask WolframAlpha
        elif "ask" in statement:

            try:

                speak("What is your question?")

                question = takeCommand()

                app_id = "R2K75H-7ELALHR35X"

                client = wolframalpha.Client(app_id)

                result = client.query(question)

                answer = next(result.results).text

                print(answer)

                speak(answer)

            except Exception as e:

                print(e)

                speak(
                    "Sorry, I could not find an answer."
                )

        # Shutdown
        elif ("log off" in statement or
              "sign out" in statement or
              "shut down" in statement):

            speak(
                "Your PC will shut down in ten seconds."
            )

            subprocess.call(
                ["shutdown", "/s", "/t", "10"]
            )
