import openai
import gtts
import speech_recognition as sr
from playsound import playsound
import pyaudio
import pygame 
import uuid
import io
from tempfile import NamedTemporaryFile

# Replace with your OpenAI API key
openai.api_key = "your-API-Key"

def generate_response(prompt):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your role is to be a highly advanced, empathetic AI assistant. Provide responses that are thoughtful, knowledgeable, and considerate, showing a level of understanding and empathy. Always maintain a polite and professional demeanor, addressing the user respectfully."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = completions.choices[0].message["content"].strip()
    return message

import os

def online_tts(text, lang="en", speed=1.0):
    output_folder = os.path.expanduser("~/Kavinsoutput")
    os.makedirs(output_folder, exist_ok=True)

    with NamedTemporaryFile(delete=False) as output_file:
        tts = gtts.gTTS(text, lang=lang, slow=False)
        tts.save(output_file.name)
        output_file.seek(0)

    pygame.init()
    pygame.mixer.init()

    # Load the sound file into a Sound object
    sound = pygame.mixer.Sound(output_file.name)

    # Set the playback speed
    sound.set_volume(1.0 / speed)

    # Play the sound with speed adjustment
    channel = sound.play()
    if channel is not None:
        channel.set_endevent(pygame.USEREVENT)
        is_playing = True
        while is_playing:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    is_playing = False
                    break
            pygame.time.Clock().tick(10)

    # Unload the music file and give the system a moment to release the file
    pygame.mixer.quit()
    pygame.time.wait(500)

    # Delete the temporary file manually
    os.remove(output_file.name)

import datetime

def get_time_based_greeting():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

import requests

def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        main = weather_data["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        weather_desc = weather_data["weather"][0]["description"]
        return f"Temperature in {city_name} is {temperature} Kelvin, Humidity is {humidity}%, and the weather is {weather_desc}"
    else:
        return "City not found"

# Replace 'your-weather-API-key' with your OpenWeatherMap API key
weather_api_key = "your-weather-API-key"

def get_latest_news(api_key, language="en", country="us"):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&language={language}&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        news_data = response.json()

        if news_data["status"] == "ok":
            headlines = [article["title"] for article in news_data["articles"][:5]]  # Fetch top 5 headlines
            return "Here are the latest news headlines: " + "; ".join(headlines)
        else:
            return "There was a problem fetching the news."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching news: {e}"

# Replace 'your-news-API-key' with your actual NewsAPI key
news_api_key = "your-news-API-key"

def recognize_speech_from_mic(recognizer, microphone, lang="en"):
    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for your voice...")
        audio = recognizer.listen(source)

    try:
        print("Transcribing your speech...")
        return recognizer.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    greeting = get_time_based_greeting()
    print(f"{greeting}, welcome to the Voice-Enabled Chatbot")
    online_tts(f"{greeting}, welcome to the Voice-Enabled Chatbot")
    history = []

    while True:
        user_input = recognize_speech_from_mic(recognizer, microphone)

        if "news update" in user_input.lower():
            news_report = get_latest_news(news_api_key)
            print(news_report)
            online_tts(news_report)
            continue
            
        if "weather" in user_input.lower():
            city_name = "Urbana"  # You can modify this to get the city from the user input
            weather_report = get_weather(city_name, weather_api_key)
            print(weather_report)
            online_tts(weather_report)
            continue

        if user_input is None:
            continue

        print(f"You: {user_input}")
        history.append(f"User: {user_input}")

        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        prompt = "\n".join(history) + "\nAI:"
        response = generate_response(prompt)
        history.append(f"AI: {response}")

        print(f"AI: {response}")

        # Convert response to speech
        online_tts(response)

if __name__ == "__main__":
    main()
