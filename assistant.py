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
