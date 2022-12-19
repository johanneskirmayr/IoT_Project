import playsound
import os
from gtts import gTTS
import time

voice_message = "Welcome to Stockholm University, I am happy to navigate you to your destination. I will also give you some insights of important spots on our way!"

# Create a text to speech object
tts = gTTS(text=voice_message, lang='en')
# Save the audio file
tts.save("voice_message.mp3")
# Play the audio file
time.sleep(2)
playsound.playsound("voice_message.mp3")
# Delete the audio file
os.remove("voice_message.mp3")

