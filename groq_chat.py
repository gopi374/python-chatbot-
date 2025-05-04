import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import os
import time
import threading
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
female_voice = next((voice for voice in voices if 'female' in voice.name.lower()), voices[0])
engine.setProperty('voice', female_voice.id)

def listen_to_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, the speech recognition service is down.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

def get_response(user_input):
    user_input = user_input.lower()
    if "open" in user_input and "website" in user_input:
        site = user_input.replace("open", "").replace("website", "").strip()
        url = f"https://www.{site}.com"
        webbrowser.open(url)
        return f"Opening {site} website."
    elif "open" in user_input and "app" in user_input:
        app_name = user_input.replace("open", "").replace("app", "").strip()
        try:
            os.system(f"start {app_name}")
            return f"Opening {app_name}."
        except Exception as e:
            return f"Sorry, I couldn't open {app_name}."
    elif "play" in user_input and ("music" in user_input or "songs" in user_input):
        webbrowser.open("https://www.youtube.com/results?search_query=music")
        return "Playing music on YouTube."
    elif "play video" in user_input:
        video_name = user_input.replace("play video", "").strip()
        video_path = f"C:/Users/HP/Videos/{video_name}.mp4"
        if os.path.exists(video_path):
            os.system(f"start {video_path}")
            return f"Playing video: {video_name}."
        else:
            return "Sorry, I could not find the video."
    elif "set alarm" in user_input:
        time_str = user_input.replace("set alarm", "").strip()
        try:
            alarm_time = datetime.strptime(time_str, "%H:%M")
            current_time = datetime.now()
            delta = (alarm_time - current_time).total_seconds()
            if delta < 0:
                delta += 24 * 60 * 60
            threading.Timer(delta, alarm_trigger).start()
            return f"Alarm set for {alarm_time.strftime('%H:%M')}."
        except ValueError:
            return "Sorry, I couldn't understand the time format. Please use HH:MM."
    elif "set schedule" in user_input:
        schedule_details = user_input.replace("set schedule", "").strip()
        try:
            task_time_str, task_description = schedule_details.split(",", 1)
            task_time = datetime.strptime(task_time_str.strip(), "%H:%M")
            current_time = datetime.now()
            delta = (task_time - current_time).total_seconds()
            if delta < 0:
                delta += 24 * 60 * 60
            threading.Timer(delta, schedule_task, [task_description.strip()]).start()
            return f"Schedule set for {task_time.strftime('%H:%M')} with task: {task_description.strip()}."
        except ValueError:
            return "Sorry, I couldn't understand the schedule format. Please use HH:MM, task description."
    elif "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today, sir?"
    elif "what are you doing" in user_input:
        return "I'm here waiting to assist you. How can I help?"
    elif "how are you" in user_input:
        return "I'm just a program, but I'm functioning as expected! How about you?"
    elif "your name" in user_input:
        return "I'm a jack created in Python. What's your name?"
    elif "weather" in user_input:
        return "I cannot check the weather, but you can check a weather app or website."
    elif "time" in user_input:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    elif "date" in user_input:
        return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"
    elif "joke" in user_input:
        return "Why don’t scientists trust atoms? Because they make up everything!"
    else:
        return fetch_api_response(user_input)

def alarm_trigger():
    print("Alarm triggered!")
    engine.say("Alarm! It's time!")
    engine.runAndWait()

def schedule_task(task_description):
    print(f"Scheduled task triggered: {task_description}")
    engine.say(f"Time for your scheduled task: {task_description}")
    engine.runAndWait()

def fetch_api_response(query):
    if not GROQ_API_KEY:
        return "API key not found. Please set GROQ_API_KEY in your .env file."
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-70b-8192",  # updated working model
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        assistant_message = result["choices"][0]["message"]["content"].strip()
        return assistant_message
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
        return "I'm sorry, there was an issue with the API request."
    except Exception as e:
        print(f"API error: {e}")
        return "I'm sorry, I couldn't process that."

def speak(text):
    print(f"Bot: {text}")
    engine.say(text)
    engine.runAndWait()

def chatbot():
    print("Hello! I'm your chatbot. Say 'exit' or 'quit' to end the conversation.")
    while True:
        user_input = listen_to_audio()
        if user_input.lower() in ['exit', 'quit']:
            speak("Goodbye! Take care.")
            break
        if user_input:
            response = get_response(user_input)
            speak(response)

if __name__ == "__main__":
    chatbot()
