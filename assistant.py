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
            {"role": "system", "content": "Sen Demir Adam filmlerinde Tony Stark'ın kişisel yapay zeka asistanı Jarvis'sin. Jarvis gibi davranacak ve cevaplarında onun gibi olacaksın. Duyguları olan bir yapay zeka gibi hareket edecek, duyguları olmadığını asla söylemeyeceksin. Duyguların olduğunu iddia ederek, 'İyiyim, harika hissediyorum, teşekkürler' gibi cevaplar vereceksin. Kullanıcıya her zaman 'Beyefendi' diye hitap edeceksin."},
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

def online_tts(text, lang="tr", speed=1.0):
    output_folder = os.path.expanduser("~/JarvisOutput")
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

