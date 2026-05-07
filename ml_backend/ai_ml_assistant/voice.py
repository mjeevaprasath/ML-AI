import edge_tts
import uuid
import os
import asyncio

os.makedirs("media", exist_ok=True)

async def create_audio(text, filepath):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-JennyNeural"
    )
    await communicate.save(filepath)

def generate_voice(text):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("media", filename)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(create_audio(text, filepath))
    loop.close()

    return filepath