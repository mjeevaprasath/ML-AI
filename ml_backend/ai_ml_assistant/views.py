from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import requests
from .models import Notes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
import asyncio
from django.views.decorators.csrf import csrf_exempt
from ml_core.ai_voice_assistant import process_command_web
import edge_tts
import uuid
import subprocess
from gtts import gTTS
from pydub import AudioSegment
import base64
import io
import edge_tts
import base64
from .voice import generate_voice
import pyttsx3
from django.http import HttpResponse

# =====================
# ENV
# =====================
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# =====================
# LOGIN / SIGNUP
# =====================
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/home/")
        else:
            return render(request, "login/index.html", {
                "error": "Invalid username or password ❌"
            })

    return render(request, "login/index.html")


def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "signup/index.html", {
                "error": "Passwords do not match ❌"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup/index.html", {
                "error": "Username already exists ❌"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/login/")

    return render(request, "signup/index.html")

# =====================
# HOME
# =====================
@login_required
def home_page(request):

# 🌐 Render online website
    if "onrender.com" in request.get_host():
        return render(request, "home/index.html")

# 💻 Localhost keeps login protection
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "home/index.html")

# =====================
# 🤖 AI
# =====================
def ask_ai(query):
    if not API_KEY:
        return "API missing"

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "system",
                        "content": "Reply short, casual, human-like. Keep it fun."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            },
            timeout=15
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return "No response"

    except Exception as e:
        print("AI ERROR:", e)
        return "Server error"


# =====================
# RENDER HOME
# =====================

def home(request):
    return HttpResponse("""
    <html>
        <head>
            <title>ML AI Backend</title>
            <link rel="icon" href="data:,">
        </head>
        <body>
            <h1>ML AI Backend Running Successfully</h1>
        </body>
    </html>
    """)

# =====================
# 📦 LENS (KEPT SAFE 😌)
# =====================
def lens_page(request):
    return render(request, "lens/index.html")

@csrf_exempt
def lens_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get("query", "")

            answer = ask_ai(query)

            return JsonResponse({
                "results": [str(answer)],
                "response": str(answer)
            })

        except Exception as e:
            print("LENS ERROR:", e)
            return JsonResponse({
                "results": ["Server error 😕"]
            })

# =====================
# CHAT API
# =====================

def chat_api(request):
    return JsonResponse({
        "response": "ML AI Chat Working"
    })  
      
# =====================
# 🎭 EMOTION DETECT
# =====================
def detect_emotion(text):
    text = text.lower()

    if any(word in text for word in ["happy", "love", "great", "awesome", "hehe", "yay"]):
        return "happy"

    elif any(word in text for word in ["angry", "hate", "stupid", "idiot", "mad"]):
        return "angry"

    elif any(word in text for word in ["sad", "sorry", "miss", "cry"]):
        return "sad"

    return "idle"


# =====================
# 🤖 PROCESS
# =====================
@csrf_exempt
def process(request):

    if request.method == "POST":

        data = json.loads(request.body)
        query = data.get("query", "")

        if not query:
            return JsonResponse({"results": ["No input"]})

        try:
            print("USER :", query)

            PERSONALITY = """
            You are a cute anime assistant named M L 💖
            Speak short, playful, cute sentences.
            Use words like hehe~, senpai, ara ara~
            """

            final_query = PERSONALITY + "\nUser: " + query

            reply = process_command_web(final_query)

            print("AI REPLY:", reply)  # ✅ correct place

            return JsonResponse({
                "results": [str(reply)],
            })

        except Exception as e:
            print("PROCESS ERROR:", e)

            return JsonResponse({
                "results": ["Something went wrong 😢"]
            })

async def tts_async(text, file_path):
    communicate = edge_tts.Communicate(
        text,
        voice="en-US-AriaNeural"   # 🔥 super natural female voice
    )
    await communicate.save(file_path)


def detect_emotion(text):
    text = text.lower()

    if any(w in text for w in ["wow", "amazing", "great", "awesome"]):
        return "happy"
    elif any(w in text for w in ["sad", "sorry", "bad"]):
        return "sad"
    elif any(w in text for w in ["angry", "what!", "why!"]):
        return "angry"
    return "neutral"


def get_voice(emotion):
    if emotion == "happy":
        return "en-US-JennyNeural"
    elif emotion == "sad":
        return "en-US-AriaNeural"
    elif emotion == "angry":
        return "en-US-GuyNeural"
    return "en-US-AriaNeural"


async def tts_async(text, file_path, voice):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(file_path)


def generate_tts(text):
    emotion = detect_emotion(text)
    voice = get_voice(emotion)

    file_path = "media/tts.wav"

    asyncio.run(tts_async(text, file_path, voice))

    return file_path, emotion
# =====================
# SPEAK API (FINAL)
# =====================

RHUBARB_PATH = r"D:\PROJECT_ML\rhubarb\rhubarb.exe"

import os
import subprocess
import json

def generate_phonemes(audio_path):

    base_dir = os.path.dirname(__file__)

    rhubarb_path = os.path.join(
        base_dir,
        "..",
        "rhubarb",
        "Rhubarb-Lip-Sync-1.14.0-Windows",
        "rhubarb.exe"
    )

    json_output = audio_path + ".json"

    command = [
        rhubarb_path,
        "-f", "json",
        "-o", json_output,
        audio_path
    ]

    subprocess.run(command, capture_output=True)

    with open(json_output, "r") as f:
        data = json.load(f)

    phonemes = []
    for cue in data["mouthCues"]:
        phonemes.append({
            "time": cue["start"],
            "phoneme": cue["value"]
        })

    return phonemes

def speak_api(request):
    text = request.GET.get("text", "")

    if not text:
        return JsonResponse({"audio": None, "phonemes": [], "emotion": "neutral"})

    # 🎤 Generate TTS
    audio_path, emotion = generate_tts(text)

    # 📦 Convert to base64
    with open(audio_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    # 💋 Lip sync
    phonemes = generate_phonemes(audio_path)

    return JsonResponse({
        "audio": audio_base64,
        "phonemes": phonemes,
        "emotion": emotion
    })
# =====================
# 🔥 HOTKEY (KEPT)
# =====================
@csrf_exempt
def hotkey(request):
    data = json.loads(request.body)
    print("HOTKEY:", data.get("name"))
    return JsonResponse({"ok": True})

# =====================
# SEARCH (ONLY ONE 😌)
# =====================
def search(request):
    query = request.GET.get("query")
    answer = ask_ai(query)

    return JsonResponse({
        "results": [answer]
    })

# =====================
# UI PAGES
# =====================
def mic(request):
    return render(request, "mic/index.html")

def logout_page(request):
    logout(request)
    return redirect("/login/")

# =====================
# NOTES
# =====================
def save_note(request):
    data = json.loads(request.body)
    text = data.get("text")

    note = Notes.objects.create(content=text)

    return JsonResponse({
        "status": "saved",
        "id": note.id
    })

def get_notes(request):
    notes = Notes.objects.all().order_by("-id")

    data = []
    for n in notes:
        data.append({
            "id": n.id,
            "content": n.content
        })

    return JsonResponse({
        "notes": data
    })