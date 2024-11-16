import pytesseract
from PIL import Image, UnidentifiedImageError
import cv2
import numpy
import pyttsx3
from gtts import gTTS
import speech_recognition as sr
import PyQt5
import time
import os
import threading

Language_map={
    "hindi":("hin","hi"),
    "english":("eng","en"),
    "french":("fra","fr"),
    "spanish":("spa","es")
}
def main(image_path,language_choice="english"):
    print("Available languages:", ', '.join(Language_map.keys()).capitalize())
    language_choice = input("Choose a language from the options above: ").lower()
    
    if language_choice.lower() in Language_map:                                                
        ocr_lang,tts_lang= Language_map[language_choice.lower()]
        print(f"Selected language :{language_choice.capitalize()}")
    else:                
        print(f"Language not supported. Default is English")
        ocr_lang,tts_lang="eng","en"
    image_data=image_scan_for_text(image_path,ocr_lang=ocr_lang)
    if image_data:
        print("\n Converting extracted text to speech....")
        text_to_speech(image_data,tts_lang=tts_lang) 

def play_audio(file_path):
    os.system(file_path if os.name=="nt"else "open "+ file_path)

def display_text(text,word_duration=0.3):
    word=text.split()
    
    
    for word in word:
        print(word , end=' ',flush=True)
        time.sleep(word_duration)
    print('\n')

def image_scan_for_text(image_path,ocr_lang="eng"):
    try:
        image=Image.open(image_path)
        extracted_text=pytesseract.image_to_string(image,lang=ocr_lang)
        print("Extracted Text:\n")
        return extracted_text
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found ")
        return ""
    except UnidentifiedImageError:
        print(f"Error: The file provided is not a valid image.")
        return ""
    except Exception as e:
        print(f"An expected error occurred: {e}")
        return ""


def text_to_speech(text,tts_lang="en"):
    if not text:
        print("No text provided for speech conversion.")
        return
    tts = gTTS(text, lang=tts_lang)
    audio_file='output.mp3'
    tts.save(audio_file)
    print(f" Audio saved as output.mp3 ")
    audio_thread=threading.Thread(target=play_audio,args=(audio_file,))
    text_thread=threading.Thread(target=display_text,args=(text,0.3))

    audio_thread.start()
    text_thread.start()

    audio_thread.join()
    text_thread.join()


if __name__=="__main__":
    main("circ.png")

   
    # print('\n')
    # if engine_choice=="pyttsx3":
    #     engine=pyttsx3.init()
    #     voices=engine.getProperty('voices')
    #     female_voice=None
    #     for voice in voices:
    #         if 'zira' in voice.name.lower() or 'female' in voice.id.lower():
    #             female_voice=voice.id
    #             break
    #     if female_voice:
    #         engine.setProperty('voice',female_voice)
    #     else:
    #         print("Female voice not found . Using default voice ")
        # engine.say(text)
        # engine.runAndWait()
    # elif engine_choice=="gtts":
    #     from gtts import gTTS
    #     tts=gTTS(text=text, lang='en',tld='com.au')
    #     tts.save("output1.mp3")
    #     os.system("start output1.mp3" if os.name=="nt" else "open output1.mp3 ")
    # else:
    #     print("Invalid TTS engine choice . Choose 'pyttsx3'or 'gtts'. ")


