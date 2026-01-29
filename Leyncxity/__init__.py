# Developed by Leyn.cx
import speech_recognition as sr
import pyttsx3
import datetime

from Leyncxity.features import date_time
from Leyncxity.features import launch_app
from Leyncxity.features import website_open
from Leyncxity.features import weather
from Leyncxity.features import wikipedia
from Leyncxity.features import news
from Leyncxity.features import send_email
from Leyncxity.features import google_search
from Leyncxity.features import google_calendar
from Leyncxity.features import note
from Leyncxity.features import system_stats
from Leyncxity.features import loc

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

class LeyncxityAssistant:
    def __init__(self):
        self.stop_speech = False
        self.system_logs = []

    def log_system(self, msg):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.system_logs.append(f"[{timestamp}] {msg}")
        if len(self.system_logs) > 50:
            self.system_logs.pop(0)

    def mic_input(self):
        try:
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    print("Listening....")
                    r.energy_threshold = 4000
                    audio = r.listen(source)
                try:
                    print("Recognizing...")
                    command = r.recognize_google(audio, language='en-in').lower()
                    print(f'You said: {command}')
                except:
                    print('Please try again')
                    return self.mic_input()
                return command
            except (OSError, AttributeError):
                return None
        except Exception as e:
            print(e)
            return False

    def tts(self, text):
        from Leyncxity.config import config
        import io
        import os
        import time
        import tempfile
        
        try:
            if config.elevenlabs_api_key and "your_elevenlabs" not in config.elevenlabs_api_key:
                try:
                    from elevenlabs import client
                    el_client = client.ElevenLabs(api_key=config.elevenlabs_api_key)
                    
                    audio_generator = el_client.text_to_speech.convert(
                        text=text,
                        voice_id=config.elevenlabs_voice_id if hasattr(config, 'elevenlabs_voice_id') else "EXAVITQu4vr4xnSDxMaL", 
                        output_format="mp3_44100_128"
                    )
                    
                    audio_bytes = b"".join(audio_generator)
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        fp.write(audio_bytes)
                        temp_path = fp.name
                    
                    import win32com.client
                    wmp = win32com.client.Dispatch("WMPlayer.OCX")
                    media = wmp.newMedia(temp_path)
                    wmp.currentPlaylist.appendItem(media)
                    wmp.controls.play()
                    
                    self.stop_speech = False
                    while wmp.playState != 1:
                        if self.stop_speech:
                            wmp.controls.stop()
                            break
                        time.sleep(0.1)
                        if wmp.playState == 0:
                            break
                    
                    os.remove(temp_path)
                    return True
                except Exception as e:
                    err_msg = f"ElevenLabs Error: {e}"
                    print(err_msg + ". Falling back to pyttsx3.")
                    self.log_system(err_msg)

            engine.say(text)
            engine.runAndWait()
            engine.setProperty('rate', 175)
            return True
        except Exception as e:
            print(f"TTS Error: {e}")
            return False

    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

    def launch_any_app(self, path_of_app):
        return launch_app.launch_app(path_of_app)

    def website_opener(self, domain):
        return website_open.website_opener(domain)

    def weather(self, city):
        try:
            res = weather.fetch_weather(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def tell_me(self, topic):
        return wikipedia.tell_me_about(topic)

    def get_recent_logs(self, count=10):
        return "\n".join(self.system_logs[-count:])

    def stop_tts(self):
        self.stop_speech = True
        try:
            import pyttsx3
            dummy = pyttsx3.init()
            dummy.stop()
        except:
            pass

    def news(self):
        return news.get_news()
    
    def send_mail(self, sender_email, sender_password, receiver_email, msg):
        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, text):
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text) 
        if date:
            return google_calendar.get_events(date, service)
    
    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        note.note(text)
    
    def system_info(self):
        return system_stats.system_stats()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country