from google.cloud import texttospeech
import os
import pygame
import time

text = """
경로 1:예상 소요시간: 14분 예상 요금: 요금 정보 없음 경북대학교북문건너까지 도보 (도보 1분) 410-1 탑승: 경북대학교북문건너 -> 경북대학교서문건너 (소요 시간: 2분)
"""
def TTS(text):
    # Set the path to the service account key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/haminse/Downloads/s2t_key.json"

    # Initialize the client
    client = texttospeech.TextToSpeechClient()

    # Set the text input and voice settings
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Make the API request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )


    #for playing audio
    # Save the audio to a file
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)


    # Initialize the mixer module
    pygame.mixer.init()

    # Load the audio file
    sound = pygame.mixer.Sound('output.mp3')

    # Play the audio
    sound.play()

    # Keep the program running while the audio is playing
    while pygame.mixer.get_busy():
        time.sleep(1)

if __name__== "__main__":
    TTS(text)