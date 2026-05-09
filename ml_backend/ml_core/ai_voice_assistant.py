# ======================================================================================================
#     - ( AI VOICE ASSISTANT ) PROJECT NAME : [ M L ]  PERSONAL ASSISTANT - 
# ======================================================================================================
import os
import sys
from pydoc import text
from urllib import response


try:
    WEB_MODE = True
    web_opened = False

    import threading

    import time
    print("ML Is Starting...")
    time.sleep(1)
    try:
        import speech_recognition as sr
    except:
        sr = None
    try:        
        import pyttsx3
    except:
        pyttsx3 = None      
    import datetime
    import webbrowser
    import random
    import requests
    import edge_tts
    import asyncio
    from langdetect import detect
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options   
        from webdriver_manager.chrome import ChromeDriverManager
    except:
        webdriver = None    
    import threading
    import logging
    #import pyautogui
    import json

#===============================
#     MEMORY SYSTEM (HYBRID) 
# ===============================

    MEMORY_FILE = "memory.json"

    def save_memory(key, value):
        data = {}
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)

        data[key] = value

        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f)

#===============================
#     GET MEMORY (HYBRID)
# ===============================

    def get_memory(key):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
               data = json.load(f)
               return data.get(key)
        return None

    def search_google_auto(query):
        webbrowser.open("https://www.google.com")
        time.sleep(3)  # wait for browser

        #pyautogui.write(query, interval=0.05)
        #pyautogui.press("enter")

        speak("Here are the results, sir")

    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

#===============================
#     -.env file- 
# ===============================
    #from dotenv import load_dotenv

# Force To Load .env correctly
    #load_dotenv()

# Warning-ah Stop Used
    #OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    import warnings
    warnings.filterwarnings("ignore")
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# =========================
#      GLOBAL STATES 
# =========================


    is_awake = False
    is_listening = False
    is_speaking = False
    is_listening_shown = False

    logging.getLogger("transformers").setLevel(logging.ERROR)

# =========================
#      PYGAME INIT 
# =========================

    try:
        import pygame
        pygame.init()
        pygame_available = True
    except:
        print("Pygame not available , skipping sound audio")
        pygame_available = False    

    if pygame_available:
        try:
            pygame.mixer.init()
            pygame.init()
            print("Audio system ready")
        except Exception as e:
            print("Audio system failed",e)
            pygame = None  
    else:
         print("Pygame not available")        
#clock = pygame.time.Clock()

# =========================
#      SPEECH RECOGNITION
# =========================
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.pause_threshold = 0.8

# =========================
#      TTS ENGINE
# =========================
    try:  
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 1)
    except:
        engine = None
        print("pyttsx3 TTS engine not available, falling back to web mode",e)    

    import sqlite3

    def init_db():
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            time TEXT
        )
        """)

        conn.commit()
        conn.close()

    def save_search(query):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO search_history (query, time) VALUES (?, ?)", (query, now))

        conn.commit()
        conn.close()

# =========================
#      ML ANIME COMMANDS
# =========================

    def run_ml_command(command):
        command = command.lower()

        if "time" in command:
            import datetime
            return "Time is " + str(datetime.datetime.now().strftime("%I:%M %p"))

        elif "hello" in command:
            return "Hello Sir 😎"

        else:
            return "Command received: " + command        

    def clean_command(command):
        command = command.lower()

    # remove wake words
        command = command.replace("Ml", "")
        command = command.replace("hey", "")
        command = command.replace("please", "")

        return command.strip()

# =========================
#      INTERNET CHECK
# =========================
    def has_internet():
      try:
         requests.get("https://www.google.com", timeout=3)
         return True
      except:
        return False

    internet = has_internet()
 
# =========================
#      SPEAK FUNCTION
# =========================

    # Anime Voice Function
    #async def amime_speak_logic(text):
    #Next
    # Used This One 'en-US-JennyNeural' for more clear voice with mood.
    # -----------------------------------------------------------------------------------------------------------------------------
    #Next 
    # Used This One 'en-US-GuyNeural' Cool And Calm (Iron Man Jarvis Style). (I like This One).
    # -----------------------------------------------------------------------------------------------------------------------------
    #Next 
    # Used This One 'en-GB-RyanNeural' for more deep and clear voice with mood.
    # -----------------------------------------------------------------------------------------------------------------------------
    # Next
    # Used This One 'en-US-AnaNeural' Cute And Soft (Classic Anime Female Lead Voice). (But I Used This One Bcz Anime Voice Chart)
    # -----------------------------------------------------------------------------------------------------------------------------
    # Next
    # Used This One 'en-US-AriaNeural' Energetic and clear voice, good for motivational and happy mood.

       #VOICE = "en-US-AnaNeural" 
       #OUTPUT_FILE = "voice.mp3"
    
       #communicate = edge_tts.Communicate(text, VOICE)
       #await communicate.save(OUTPUT_FILE)

    # Play the sound
        #pygame.mixer.music.load(OUTPUT_FILE)
       #pygame.mixer.music.play()

      #while pygame.mixer.music.get_busy():
            #await asyncio.sleep(0.1)
    
       #pygame.mixer.music.stop()
       #File was delete then unload now
       #pygame.mixer.music.unload()
       #if os.path.exists(OUTPUT_FILE):
            #os.remove(OUTPUT_FILE)

# Main Speak Wrapper
    def speak(text):
        global is_speaking, WEB_MODE

    # 🌐 Frontend mode → no backend voice
        if WEB_MODE:
            print(f"🤖 (WEB) ML: {text}")
            return text

    # 🖥️ Local fallback (NO EDGE-TTS, NO PYTTSX3)
        print(f"🤖 ML: {text}")
        return text
# =========================
#      LISTEN FUNCTION
# =========================

    def listen():
        return ""
        
# =========================
#      SENTIMENT MODEL
# =========================
    sentiment_model = None
    model_loaded = False

    def get_sentiment_model():
        global sentiment_model, model_loaded

        if not model_loaded:
          from transformers import pipeline
          sentiment_model = pipeline(
            "sentiment-analysis",
            model="sshleifer/tiny-distilbert-base-uncased-finetuned-sst-2-english"
          )
          model_loaded = True 

        return sentiment_model

# =========================
#      APPS
# =========================
    apps = {
      "chrome": "chrome.exe",
      "notepad": "notepad.exe",
      "calculator": "calc.exe",
      "cmd": "cmd.exe",
      "vs code": "Code.exe",
      "edge": "msedge.exe"
      }

# =========================
#      DETECT INTENT
# =========================
    def detect_intent(command):
        command = command.lower()
        if any(word in command for word in ["open", "start", "launch"]):
           return "open"
        elif any(word in command for word in ["close", "stop", "exit"]):
           return "close"
        elif any(word in command for word in ["play", "watch"]):
           return "play"
        elif "time" in command:
           return "time"
        else:
           return "unknown"

# =========================
#      SMART PARSE
# =========================
    def smart_parse(command):
        command = command.lower()
    
        ai_keywords = ["what is", "who is", "how to", "why is", "explain", "define", "tell me about","what are", "who are", "how do", "why do", "can you", "could you", "would you", "do you know", "is it true that"]
        if any(word in command for word in ai_keywords):
          return [] # Empty list anupuna thaan loop AI-ku pogum!

    # YouTube Commands logic
        if "play" in command or "search" in command:
        # "play" and "search" words-ah mattum remove pannanum
           query = command.replace("play", "").replace("search", "").strip()
           return [("youtube", query)]
        
        return []
# -------------------------
#      EXECUTE SMART COMMAND
# -------------------------
    def execute_smart_command(command):
        actions = smart_parse(command)
    
        # 1. EMPTY CHECK (AI-ku poga idhu thaan vazhi)
        if not actions:
           return "not_found"

        for action, value in actions:
            # 2. SEARCH LOGIC
            if action == "search":
               speak(f"Searching {value}")
               webbrowser.open(f"https://www.google.com/search?q={value}")
               return "done"

            # 3. YOUTUBE LOGIC
            elif action == "youtube":
                if value:
                   speak(f"Ok sir, opening YouTube and playing {value}")
                   threading.Thread(target=play_youtube_video, args=(value,), daemon=True).start()
                   return "done"
                else:
                   speak("Ok sir, opening YouTube")
                   webbrowser.open("https://youtube.com")
                   return "done"

            # 4. OPEN APPS LOGIC
            elif action == "open":
                if value:
                    if value in apps:
                       speak(f"Opening {value}")
                       os.system(f"start {apps[value]}")
                       return "done"
                    else:
                       speak(f"I don't know how to open {value}")
                       return "done"
            else:
                speak("What should I open sir?")
                return "done"

        return "not_found"
# -------------------------
#      PLAY YOUTUBE
# -------------------------
    def play_youtube_video(query):
    #  SMART MOOD BASED SEARCH
        if "motivation" in query:
           query = "motivational speech tamil"
        elif "sad" in query:
           query = "sad songs tamil"
        elif "study" in query or "focus" in query:
           query = "study music for concentration"
        elif "sleep" in query:
           query = "relaxing sleep music"
        elif "gym" in query:
           query = "workout motivation music"
        elif "love" in query:
           query = "romantic tamil songs"
        elif "angry" in query:
           query = "calm music to relax mind"


        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")

        driver = webdriver.Chrome(
          service=Service(ChromeDriverManager().install()),
          options=chrome_options
        )

        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        driver.get(search_url)

        time.sleep(3)

        try:
           first_video = driver.find_element(By.ID, "video-title")
           first_video.click()
        except:
           speak("Could not play the video")

# -------------------------
#      EXECUTE COMMAND
# -------------------------
    def execute_command(command):
        command = command.lower()


# =====================
# STOP COMMAND (WEB MODE RESET)
# =====================
        if "stop" in command or "podhum" in command or "exit" in command:
            global WEB_MODE, is_awake
            WEB_MODE = False
            is_awake = False
            return "stopped"

# =====================
# MEMORY SYSTEM (HYBRID)
# =====================        

        elif "my name is" in command:
            name = command.replace("my name is", "").strip()
            save_memory("name", name)
            speak(f"Nice to meet you {name}")
            return "done"

        elif "what is my name" in command:
            name = get_memory("name")
            if name:
                speak(f"Your name is {name}")
            else:
                speak("I don't know your name yet")
            return "done"
# =====================
# CLOSE APPS (HYBRID)
# =====================
        elif "close" in command:

            if "chrome" in command or "google" in command:
                os.system("taskkill /f /im chrome.exe")
                speak("Closing Chrome")

            elif "notepad" in command:
                os.system("taskkill /f /im notepad.exe")
                speak("Closing Notepad")

            elif "cmd" in command:
                os.system("taskkill /f /im cmd.exe")
                speak("Closing command prompt")

            elif "explorer" in command:
                os.system("taskkill /f /im explorer.exe")
                speak("Closing file explorer")

            else:
            # fallback (ANY APP)
                app_name = command.replace("close", "").strip()

                if "google" in app_name:
                    app_name = "chrome"

                close_any_app(app_name)

            return "done"
        
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")
            return "done"
        
        elif "date" in command or "today" in command:
            today = datetime.datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today is {today}")
            return "done"

# =====================
# SEARCH GOOGLE
# =====================
        elif "search" in command:

            query = command.replace("search", "") \
                    .replace("in google", "") \
                    .replace("for", "") \
                    .strip()
            if query == "":
                    speak("What should I search, sir?")
                    return "done"

    # SAVE TO DB
            save_search(query)

    # ✅ OPEN CHROME SEARCH
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching {query} in Chrome")
            return "done" 

# =====================
# OPEN APPS (HYBRID)
# =====================
        elif "open" in command:

            if "notepad" in command:
                os.system("notepad")
                speak("Opening Notepad")

            elif "chrome" in command or "google" in command:
                webbrowser.open("https://www.google.com")
                speak("Opening Google")

            elif "youtube" in command:
                webbrowser.open("https://www.youtube.com")
                speak("Opening YouTube")

            elif "whatsapp" in command:
                webbrowser.open("https://web.whatsapp.com")
                speak("Opening WhatsApp")

            elif "gmail" in command or "email" in command:
                webbrowser.open("https://mail.google.com")
                speak("Opening Gmail")

            elif "file explorer" in command:
                os.system("explorer")
                speak("Opening File Explorer")

            elif "cmd" in command:
                os.system("start cmd")
                speak("Opening command prompt")

            elif "settings" in command:
                os.system("start ms-settings:")
                speak("Opening Settings")

            elif "photos" in command:
                os.system("start ms-photos:")
                speak("Opening Photos")

            else:
                app_name = command.replace("open", "").strip()
                open_any_app(app_name)

            return "done"

# ======================
# TYPE ANYWHERE (HYBRID)
# ====================== 
      
        elif "type" in command:
            text = command.replace("type", "").strip()
            if text:
                type_anywhere(text)
                speak("Typing completed")
            else:
                speak("What should I type, sir?")
            return "done"

# ========================
# REPLY ANYWHERE (HYBRID)
# ========================

        elif "reply" in command:
            text = command.replace("reply", "").strip()
            auto_reply(text)
            speak("Message sent")
            return "done"

        return "not_found"

# ========================
#      PLAY MUSIC
# ========================
    def play_music():
        possible_paths = [os.path.expanduser("~/Music"), "C:\\Music", "D:\\Music"]
        music_folder = None
    
        for path in possible_paths:
            if os.path.exists(path):
               music_folder = path
               break
            
        if not music_folder: # Loop-ku outside check processes
            speak("I couldn't find your music folder")
            return
        
# ====================================
#  OPEN AND CLOSE ANY APP (FALLBACK)
# ====================================        

    def open_any_app(app_name):
        app_name = app_name.strip()
        os.system(f"start {app_name}")
        speak(f"Opening {app_name}")  

    def close_any_app(app_name):
        app_name = app_name.strip() + ".exe"
        os.system(f"taskkill /f /im {app_name}")
        speak(f"Closing {app_name}")

# ===========================
#  TYPE ANYWHERE (FALLBACK)
# =========================== 

    def type_anywhere(text):
        #pyautogui.write(text, interval=0.03)
        print("Typing disabled on Render")

# =================================
#  AUTO REPLY ANYWHERE (FALLBACK)
# =================================

    def auto_reply(text):
        #pyautogui.write(text, interval=0.03)
        #pyautogui.press("enter")
        print("Auto-reply disabled on Render")            

# ==========================
#      AI FUNCTION 
# ==========================

    GROQ_API_KEY = "YOUR_API_KEY_HERE"

    import requests

    def ask_ai(prompt):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            return "API key missing sir 😕"
 
        if not prompt or prompt.strip() == "":
            return "Please say something sir 😅"

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are not a robot. You are a friendly anime AI companion. " 
                                            "Talk like a close friend. Use fun tone. Avoid formal language. "
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    },
                    timeout=20
                )

        # ✅ Status check
            if response.status_code != 200:
               print("API ERROR:", response.text)
               return "Server problem sir 😕"

            data = response.json()

        # ✅ Safe parsing
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"].strip()
            else:
                print("Invalid response:", data)
                return "AI not responding properly sir 😕"

        except requests.exceptions.Timeout:
            return "Server timeout sir ⏳"

        except requests.exceptions.ConnectionError:
            return "No internet connection sir 🌐"

        except Exception as e:
            print("ERROR:", e)
            return "Unexpected error sir 😕"
            
# ========================
#      STARTUP LOGIC
# ========================
    def start_ml():
        try:
            # Clean startup to avoid double printing
            print("ML SYSTEM INITIALIZED...")
            time.sleep(1)
            speak("ML is ready. Listening for wake word, tell me.")
            return True
        except Exception as e:
            print(f"Startup error: {e}")
            return False

    start_ml()

#===============================
#     -.env file- 
# ===============================
    
    import os
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#==========================
#   WEB COMMAND FUNCTION 
#==========================
    previous_messages = []

    def process_command_web(text):

        global previous_messages

        text = text.lower()

        if "stop" in text:
            return "Stopped"

        try:
        # ✅ ADD USER MESSAGE TO MEMORY
            previous_messages.append({
                "role": "user",
                "content": text
            })

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # 🔥 faster + working model

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Talk like a cute anime assistant."
                            "Keep replies VERY short (1-2 lines only)."
                            "Be casual, friendly, slightly teasing."
                            "Use simple words like a human friend."
                            "No long explanations."
                        )
                    }
                ] + previous_messages[-6:],   # 🔥 last 6 messages only

                temperature=0.8,
                max_tokens=40
            )

            reply = completion.choices[0].message.content.strip()

        # ✅ SAVE AI RESPONSE ALSO
            previous_messages.append({
                "role": "assistant",
                "content": reply
            })

            print("ML REPLY:", reply)

            return reply

        except Exception as e:
            print("GROQ ERROR:", e)
            return "Oops 😅 something went wrong"
    
# WAKE WORDS & MAIN LOOP
    wake_words = ["ml on", "hey ml", "ml"]
    is_awake = False
    running = True

# =========================
#      MAIN LOOP (FIXED)
# =========================
    if __name__ == "__main__":
        start_ml()

        while running:
            try:
            # existing loop code
                if not is_awake:
                    command = listen()
                    if not command:
                        continue

                    if any(word in command for word in wake_words):
                        is_awake = True
                        speak("Welcome back hai")

                    continue

                command = listen()
                if not command:
                    continue

                command = clean_command(command)

                if "stop" in command:
                    is_awake = False
                    continue

                result = execute_command(command)

                if result == "not_found":
                    smart_result = execute_smart_command(command)
                else:
                    smart_result = "done"

                if smart_result == "not_found":
                    ai_response = ask_ai(command)
                    speak(ai_response)

            except Exception as e:
                print(e)

except KeyboardInterrupt:
    print("\n[!] ML is going offline. Goodbye, Sir.")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

    except Exception as e:
    # The Real Time Error Log (Hidden from User)
        print(f"\n[!] Hidden System Error: {e}")    