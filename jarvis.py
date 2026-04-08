print("JARVIS IS STARTING...")

try:
# ===============================
#     -JARVIS PERSONAL ASSISTANT- 
# ===============================
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
  
    import speech_recognition as sr
    import pyttsx3
    import time
    import datetime
    import webbrowser
    import random
    import requests
    from langdetect import detect
    from gtts import gTTS
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options   
    from webdriver_manager.chrome import ChromeDriverManager
    import threading
    import logging

    import sys
    import google.genai as genai
    api_key= "AIzaSyCs97iiIikwzhH-Y7XpseYXSgklyGUa11I"

    if not api_key:
       print("API KEY MISSING....")
    else:
       client = genai.Client(api_key=api_key)
       print("JARVIS IS READY...")   


    import warnings
    warnings.filterwarnings("ignore")
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# -------------------------
#      GLOBAL STATES 
# -------------------------


    is_awake = False
    is_listening = False
    is_speaking = False
    is_listening_shown = False

    logging.getLogger("transformers").setLevel(logging.ERROR)

# -------------------------
#      PYGAME INIT 
# -------------------------

    try:
       import pygame
       pygame.init()
    except:
       print("Pygame not available , skipping sound audio")
       pass    

    if pygame:
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

# -------------------------
#      SPEECH RECOGNITION
# -------------------------
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8

# -------------------------
#      TTS ENGINE
# -------------------------  
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1)

    def clean_command(command):
      command = command.lower()

    # remove wake words
      command = command.replace("jarvis", "")
      command = command.replace("hey", "")
      command = command.replace("please", "")

      return command.strip()

# -------------------------
#      INTERNET CHECK
# -------------------------
    def has_internet():
      try:
         requests.get("https://www.google.com", timeout=3)
         return True
      except:
        return False

    internet = has_internet()
 
# -------------------------
#      SPEAK FUNCTION
# -------------------------
    def speak(text, mood="neutral"):
      global is_speaking

      if is_speaking:   # LOCK MIC
        return
   
      is_speaking = True


      if mood == "happy":
        text = "Hey! " + text
      elif mood == "sad":
        text = "Hmm... " + text

      if internet:
        try:
            filename = "voice.mp3"
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(filename)

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.stop()
            os.remove(filename)

        except:
            engine.say(text)
            engine.runAndWait()
      else:
        engine.say(text)
        engine.runAndWait()

      time.sleep(0.5)  # small buffer
      is_speaking = False   # UNLOCK

    def ask_gpt(prompt):
        try:
         response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"You are Jarvis. Speak short and clear.\nUser: {prompt}"
         )

         return response.text.strip()

        except Exception as e:
          print("AI ERROR:", e)
          return "Sorry sir, I couldn't think right now."
# -------------------------
#      LISTEN FUNCTION
# -------------------------
    def listen():

        r.pause_threshold = 0.8
        r.energy_threshold = 300

        global is_speaking, is_listening_shown

        if is_speaking:
          time.sleep(0.3)
          return ""

    # Show only once
        if not is_listening_shown:
          print("🎤 Listening...")
          is_listening_shown = True
 
        with sr.Microphone() as source:
          r.adjust_for_ambient_noise(source, duration=0.5)

          try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
          except:
            return ""

        try:
           command = r.recognize_google(audio).lower()
           print("You said:", command)

           is_listening_shown = False   # RESET after hearing

           if not command:
             time.sleep(0.5)
             return ""

           return command

        except:
           is_listening_shown = False
           return ""
# -------------------------
#      SENTIMENT MODEL
# -------------------------
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

# -------------------------
#      APPS
# -------------------------
    apps = {
      "chrome": "chrome.exe",
      "notepad": "notepad.exe",
      "calculator": "calc.exe",
      "cmd": "cmd.exe",
      "vs code": "Code.exe",
      "edge": "msedge.exe"
      }

# -------------------------
#      DETECT INTENT
# -------------------------
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

# -------------------------
#      SMART PARSE
# ------------------------- 
    def smart_parse(command):
        command = command.lower()
        actions = []

    #  FIX CLEANING
        command = command.replace("search on youtube", "")
        command = command.replace("search youtube", "")
        command = command.replace("on youtube", "")
        command = command.replace("youtube", "")

    #  REMOVE JUNK WORDS
        for word in ["search", "play", "open"]:
           command = command.replace(word, "")

           query = command.strip()

           if query:
             actions.append(("youtube", query))
           else:
             actions.append(("youtube", ""))
 
           return actions
# -------------------------
#      EXECUTE SMART COMMAND
# -------------------------
    def execute_smart_command(command):
        actions = smart_parse(command)
 
        for action, value in actions:

          if action == "search":
            speak(f"Searching {value}")
            webbrowser.open(f"https://www.google.com/search?q={value}")
            return "done"

        
          elif action == "youtube":
            if value:
               speak(f"Ok sir, opening YouTube and playing {value}")
            else:
               speak("Ok sir, opening YouTube")

            threading.Thread(target=play_youtube_video, args=(value,), daemon=True).start()
            return "done"


          elif action == "open":
            if value:
              if value in apps:
                speak(f"Opening {value}")
                os.system(f"start {apps[value]}")
              else:
                 speak(f"I don't know how to open {value}")
           
            else:
                speak("What should I open sir?")
                return "done"
        
          else:
               speak("I didn't understand that part")
               return "done"

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
       parts = command.split(" and ")

       for part in parts:

         intent = detect_intent(part)

        # =========================
        # OPEN
        # =========================
         if intent == "open":

            if "youtube" in part and "search" in part:
                query = part.replace("open youtube", "").replace("search", "").strip()
                speak(f"Opening YouTube and searching {query}")
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

            elif "youtube" in part:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com")

            elif "google" in part:
                speak("Opening Google")
                webbrowser.open("https://google.com")

            elif "notepad" in part:
                os.system("start notepad")
                speak("Opening notepad")

            elif "cmd" in part:
                os.system("start cmd")
                speak("Opening command prompt")

            elif "vs code" in part:
                os.system("start code")
                speak("Opening VS Code")

            #  Apps dictionary
            else:
                for app in apps:
                    if app in part:
                        speak(f"Opening {app}")
                        os.system(f"start {apps[app]}")
                        break

            if "music" in part:
                play_music()

        # =========================
        # CLOSE
        # =========================
         elif intent == "close":
            for app in apps:
                if app in part:
                    speak(f"Closing {app}")
                    os.system(f"taskkill /f /im {apps[app]}")
                    break

        # =========================
        # PLAY
        # =========================
         elif intent == "play":
            query = part.replace("play", "").strip()
            if query:
                speak(f"Playing {query} on YouTube")
                play_youtube_video(query)
            else:
                speak("What should I play sir?")

        # =========================
        # SEARCH
        # =========================
         elif intent == "search":
            query = part.replace("search", "").strip()
            speak(f"Searching {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")

        # =========================
        # TIME
        # =========================
         elif intent == "time":
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")

        # =========================
        # SYSTEM
        # =========================
         elif "shutdown" in part:
            speak("Shutting down the computer")
            os.system("shutdown /s /t 5")

         elif "restart" in part:
            speak("Restarting the computer")
            os.system("shutdown /r /t 5")

        # =========================
        # EXIT
        # =========================
         elif "bye" in part or "stop" in part:
            speak("Going to sleep")
            return "sleep"

         else:
            speak("Sorry sir I don't know that command")

         return None
# -------------------------
#      PLAY MUSIC
# -------------------------
    def play_music():
         possible_paths = [
           os.path.expanduser("~/Music"),
           "C:\\Music",
           "D:\\Music"
         ]
         music_folder = None
         for path in possible_paths:
            if os.path.exists(path):
              music_folder = path
              break
            if not music_folder:
              speak("I couldn't find your music folder")
              return
            
         songs = [song for song in os.listdir(music_folder) if song.endswith((".mp3", ".wav"))]
         if songs:
           song = random.choice(songs)
           speak("Playing music")
           os.startfile(os.path.join(music_folder, song))
         else:
           speak("No songs found")

# -------------------------
#      STARTUP
# -------------------------
    print("Jarvis is ready...")
    speak("Jarvis is ready")

    wake_word = ["jarvis on","hey jarvis","jarvis"]
    running = True
    is_awake = False
# =========================
#      MAIN LOOP
# =========================

    def wake_listener():
      global is_awake

      while True:
        if not is_awake:
            command = listen()

            if command and any(word in command for word in wake_word):
                print("WAKE WORD DETECTED ")

                is_awake = True #SET FIRST.....

                time.sleep(0.3)

                speak("Hello sir! I am listening.")
                time.sleep(0.3)
                speak("how can i help you sir ?")
                #time.sleep(0.3)
                speak("Waiting for your command")
                print("Jarvis : Waiting for your command....")
                #is_listening_shown = False #RESET......
                #time.sleep(1)
                #is_awake = True

        else:        

           time.sleep(0.3)




    def command_listener():
      global is_awake, running

      while running:
        if is_awake:
            try:   

                # 🎤 FIRST LISTEN
                command = listen()

                if "jarvis" in command:
                    speak("Yes sir")
    
                    command = listen()
                    command = clean_command(command)

                    execute_command(command)

                if not command or len(command.strip()) < 2:
                    continue

                #  REMOVE WAKE WORD
                for word in wake_word:
                    if word in command:
                        command = command.replace(word, "").strip()

                #  WAIT FOR FULL SENTENCE (SECOND LISTEN)
                time.sleep(1.5)
                extra = listen()

                while extra:

                    command += " " + extra
                    extra = listen()

                #  SMART EXECUTION
                result = execute_command(command)
                if result == "sleep":
                    is_awake = False
                    continue

                smart_result = execute_smart_command(command)

                #  EXIT COMMAND
                if command.lower() in ["bye", "ok bye", "stop"]:
                    speak("Going to sleep sir")
                    is_awake = False
                    continue

                #  SENTIMENT ANALYSIS
                try:
                    if sentiment_model is None:
                        get_sentiment_model()

                    result_sentiment = sentiment_model(command)
                    label = result_sentiment[0]["label"]
                except:
                    label = None

                if label == "NEGATIVE":
                    mood = "sad"
                    reply_prefix = "I'm here for you sir. "
                elif label == "POSITIVE":
                    mood = "happy"
                    reply_prefix = "That's great to hear sir! "
                else:
                    mood = "neutral"
                    reply_prefix = ""

                #  BASIC CONVERSATION
                if "how are you" in command:
                    reply = "I am always fine sir. What about you?"
                elif "your name" in command:
                    reply = "I am Jarvis, your personal assistant."
                elif "time" in command:
                    now = datetime.datetime.now().strftime("%H:%M")
                    reply = f"The time is {now}"
                else:
                    reply = ""

                #  FINAL RESPONSE
                if reply:
                    final_reply = reply_prefix + reply
                else:
                    ai_reply = ask_gpt(command)
                    final_reply = reply_prefix + ai_reply

                print(f"🤖 Jarvis: {final_reply}")
                speak(final_reply, mood)

            except Exception:   
                print("Runtime issuse handled")
                speak("Please wait sir , something went wrong")
                continue

        else:
            time.sleep(0.1)
#print("Jarvis Is Ready...")

# =========================
#   GPT TEST
# =========================

      response = ask_gpt("say hello like jarvis")
      print("GPT TEST:", response)       

# =========================
#   START JARVIS THREADS
# =========================

    threading.Thread(target=wake_listener, daemon=True).start()
    threading.Thread(target=command_listener, daemon=True).start()

    while True:
     time.sleep(1)

except KeyboardInterrupt:
    print("\nJarvis stopped safely")
    try:
        speak("Shutting down sir")
    except:
        pass

except Exception as e:
    print("⚠️ Hidden Error:", e)
    try:
        speak("Please wait sir, some error occurred")
    except:
        pass             