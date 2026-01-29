# Developed by Leyn.cx
from Leyncxity import LeyncxityAssistant
import re
import os
import random
import pprint
import datetime
import requests
import sys
import urllib.parse  
import pyjokes
import time
import pyautogui
import wolframalpha
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from Leyncxity.features.gui import Ui_MainWindow
from Leyncxity.config import config
from Leyncxity.features.ai_agent import LeyncxityAI

obj = LeyncxityAssistant()

GREETINGS = ["hello leyncxity", "leyncxity", "wake up leyncxity", "you there leyncxity", "time to work leyncxity", "hey leyncxity",
             "ok leyncxity", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'myself': 're5408887@gmail.com',
    'my official email': 're5408887@gmail.com',
    'my second email': 're5408887@gmail.com',
    'my official mail': 're5408887@gmail.com',
    'my second mail': 're5408887@gmail.com'
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]

class MainThread(QThread):
    chatSignal = pyqtSignal(str) 
    statusSignal = pyqtSignal(str) 
    speakingSignal = pyqtSignal(bool) 
    moodSignal = pyqtSignal(str) 

    def __init__(self):
        super(MainThread, self).__init__()
        self.ai = LeyncxityAI()
        self.pending_command = None

    def receive_input(self, text):
        obj.stop_tts()
        self.pending_command = text

    def run(self):
        self.TaskExecution()

    def speak(self, text):
        self.chatSignal.emit(f"LEYNCXITY: {text}")
        self.speakingSignal.emit(True)
        obj.tts(text)
        self.speakingSignal.emit(False)

    def startup(self):
        self.statusSignal.emit("SYSTEM: INITIALIZING")
        self.speak("Initializing Leyncxity. Starting all system applications and examining core processors.")
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<=12:
            self.speak("Good Morning")
        elif hour>12 and hour<18:
            self.speak("Good afternoon")
        else:
            self.speak("Good evening")
        self.speak("I am ready to help sir.")
        self.statusSignal.emit("SYSTEM: ONLINE")

    def TaskExecution(self):
        self.startup()

        while True:
            if self.pending_command:
                command = self.pending_command
                self.pending_command = None
            else:
                command = obj.mic_input()
                if not command:
                    self.statusSignal.emit("SYSTEM: IDLE")
                    self.moodSignal.emit("idle")
                    time.sleep(0.5)
                    continue
                self.moodSignal.emit("listening")

            if "goodbye" in command or "offline" in command or "bye" in command:
                self.speak("Alright sir, going offline. It was nice working with you")
                sys.exit()

            try:
                self.statusSignal.emit("SYSTEM: PROCESSING")
                self.moodSignal.emit("thinking")
                current_input = command
                for _ in range(3): 
                    response = self.ai.chat(current_input)
                    if not response: break
                    
                    print(f"AI Response: {response}")
                    tool_result = self.perform_action(response)
                    
                    if tool_result:
                        current_input = f"SYSTEM TOOL OUTPUT: {tool_result}"
                        self.statusSignal.emit("SYSTEM: ANALYZING")
                        continue
                    else:
                        break

                self.moodSignal.emit("success")
            except Exception as e:
                print(f"Error executing AI command: {e}")
                self.moodSignal.emit("error")
                self.speak("Sorry sir, I had a glitch.")
            
            self.statusSignal.emit("SYSTEM: ONLINE")
            self.moodSignal.emit("idle")

    def perform_action(self, response):
        action = response.get('action')
        params = response.get('params', {})
        reply = response.get('reply')

        if reply:
            self.speak(reply)

        if action == 'tell_time':
            time_c = obj.tell_time()
            self.speak(f"The time is {time_c}")
            
        elif action == 'tell_date':
            date_c = obj.tell_me_date()
            self.speak(f"Today is {date_c}")
            
        elif action == 'launch_app':
            app_name = params.get('app_name', '').lower()
            dict_app = {
                'chrome': 'C:/Program Files/Google/Chrome/Application/chrome',
                'notepad': 'notepad',
                'calculator': 'calc'
            }
            path = dict_app.get(app_name)
            if path:
                obj.launch_any_app(path_of_app=path)
            else:
                self.speak(f"I don't know the path for {app_name}")

        elif action == 'open_website':
            domain = params.get('domain')
            if domain:
                obj.website_opener(domain)

        elif action == 'get_weather':
            city = params.get('city')
            if city:
                res = obj.weather(city)
                self.speak(res)

        elif action == 'wikipedia_search':
            query = params.get('query')
            if query:
                res = obj.tell_me(query)
                self.speak(res)

        elif action == 'get_news':
            news_res = obj.news()
            self.speak('Top headlines:')
            for i, article in enumerate(news_res):
                if i >= 3: break
                self.speak(article['title'])

        elif action == 'google_search':
            query = params.get('query')
            if query:
                obj.search_anything_google(f"search google for {query}")

        elif action == 'play_youtube':
            video = params.get('video_query')
            if video:
                import pywhatkit
                pywhatkit.playonyt(video)

        elif action == 'send_email':
            sender = config.email
            pwd = config.email_password
            recipient_name = params.get('recipient_name')
            subject = params.get('subject')
            message = params.get('message')
            receiver = EMAIL_DIC.get(recipient_name)
            if receiver:
                obj.send_mail(sender, pwd, receiver, f"Subject: {subject}\n\n{message}")
                self.speak("Email sent.")
            else:
                self.speak("Unknown recipient.")

        elif action == 'take_note':
            text = params.get('text')
            if text: obj.take_note(text)

        elif action == 'system_info':
            self.speak(obj.system_info())

        elif action == 'get_location':
            place = params.get('place')
            try:
                _, _, dist = obj.location(place)
                self.speak(f"{place} is {dist} km away.")
            except:
                self.speak("Could not find location.")

        elif action == 'get_my_location':
            try:
                city, state, country = obj.my_location()
                self.speak(f"You are in {city}, {state}, {country}")
            except:
                self.speak("Could not determine location.")

        elif action == 'take_screenshot':
            name = params.get('filename', 'sc_shot')
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            self.speak("Screenshot saved.")

        elif action == 'play_music':
            music_dir = "F://Songs//Imagine_Dragons"
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                for song in songs:
                    os.startfile(os.path.join(music_dir, song))
                    break

        elif action == 'remember_fact':
            key = params.get('key')
            value = params.get('value')
            if key and value:
                from Leyncxity.features.memory_manager import update_memory
                update_memory(key, value)
                self.speak(f"I have successfully committed that to my core memory, sir.")

        elif action == 'find_file':
            filename = params.get('filename')
            if filename:
                from Leyncxity.features.file_manager import find_file
                self.speak(f"Searching for {filename}...")
                results = find_file(filename)
                if results:
                    self.speak(f"I found {len(results)} matches for {filename}. I've listed the locations in your console, sir.")
                    for res in results:
                        self.chatSignal.emit(f"PATH: {res}")
                    return f"FOUND_FILES: {results}"
                else:
                    self.speak(f"Sorry sir, I couldn't find {filename} on your system.")
                    return "FILE_NOT_FOUND"

        elif action == 'create_file':
            path = params.get('path')
            content = params.get('content', '')
            if path:
                from Leyncxity.features.file_manager import create_file
                res = create_file(path, content)
                if res is True:
                    self.speak(f"File created successfully at {path}.")
                else:
                    self.speak(f"Failed to create file: {res}")

        elif action == 'rename_file':
            old = params.get('old_path')
            new = params.get('new_path')
            if old and new:
                from Leyncxity.features.file_manager import rename_file
                res = rename_file(old, new)
                if res is True:
                    self.speak(f"File renamed from {old} to {new}.")
                else:
                    self.speak(f"Failed to rename file: {res}")

        elif action == 'delete_file':
            path = params.get('path')
            if path:
                from Leyncxity.features.file_manager import delete_file
                res = delete_file(path)
                if res is True:
                    self.speak(f"File at {path} has been deleted.")
                else:
                    self.speak(f"Failed to delete file: {res}")

        elif action == 'list_directory':
            path = params.get('path')
            if path:
                from Leyncxity.features.file_manager import list_directory
                res = list_directory(path)
                if isinstance(res, dict):
                    files = res.get('files', [])
                    folders = res.get('folders', [])
                    self.speak(f"I've retrieved the contents of {path}, Ryan. There are {len(files)} files and {len(folders)} folders.")
                    self.chatSignal.emit(f"FOLDERS: {', '.join(folders)}")
                    self.chatSignal.emit(f"FILES: {', '.join(files)}")
                    return res 
                else:
                    self.speak(f"Could not list directory: {res}")
                    return f"ERROR: {res}"

        elif action == 'find_folder':
            foldername = params.get('foldername')
            if foldername:
                from Leyncxity.features.file_manager import find_folder
                self.speak(f"Searching for folder {foldername}...")
                results = find_folder(foldername)
                if results:
                    self.speak(f"I found {len(results)} matching folders for {foldername}. Details are in the chat.")
                    for res in results:
                        self.chatSignal.emit(f"PATH: {res}")
                    return f"FOUND_FOLDERS: {results}"
                else:
                    self.speak(f"Sorry sir, I couldn't find the folder {foldername} on your system.")
                    return "FOLDER_NOT_FOUND"

        elif action == 'create_folder':
            path = params.get('path')
            if path:
                from Leyncxity.features.file_manager import create_folder
                res = create_folder(path)
                if res is True:
                    self.speak(f"Folder created successfully at {path}.")
                else:
                    self.speak(f"Failed to create folder: {res}")

        elif action == 'delete_folder':
            path = params.get('path')
            if path:
                from Leyncxity.features.file_manager import delete_folder
                res = delete_folder(path)
                if res is True:
                    self.speak(f"Folder at {path} and all its contents have been deleted.")
                else:
                    self.speak(f"Failed to delete folder: {res}")

        elif action == 'open_folder':
            path = params.get('path')
            if path:
                from Leyncxity.features.file_manager import open_folder
                res = open_folder(path)
                if res is True:
                    self.speak(f"Opening folder: {path}")
                else:
                    self.speak(f"Could not open folder: {res}")

        elif action == 'read_file_content':
            path = params.get('path')
            if path:
                from Leyncxity.features.summarizer import get_file_content
                self.speak(f"Reading content of {os.path.basename(path)}...")
                content = get_file_content(path)
                return content 

        elif action == 'system_control':
            cmd = params.get('command')
            val = params.get('value')
            from Leyncxity.features.system_control import set_volume, set_brightness, mute_system, lock_pc
            
            if cmd == 'volume':
                set_volume(val)
                self.speak(f"System volume adjusted to {val} percent.")
            elif cmd == 'brightness':
                set_brightness(val)
                self.speak(f"Screen brightness set to {val} percent.")
            elif cmd == 'mute':
                mute_system(val)
                self.speak("System muted." if val else "System unmuted.")
            elif cmd == 'lock':
                self.speak("Locking mainframe. Goodbye for now.")
                lock_pc()
            elif cmd == 'sleep':
                from Leyncxity.features.system_control import suspend_pc
                self.speak("Mainframe going to sleep. Goodbye sir.")
                suspend_pc()

        elif action == 'chrome_control':
            cmd = params.get('cmd')
            url = params.get('url')
            query = params.get('query')
            act = params.get('action')
            target = params.get('target')
            val = params.get('value')
            from Leyncxity.features.chrome_automation import chrome_control
            self.speak(f"Executing Chrome automation: {cmd}...")
            res = chrome_control(cmd, url, query, act, target, val)
            return res

        elif action == 'get_path_info':
            path = params.get('path')
            if path:
                from Leyncxity.features.file_manager import get_path_info
                res = get_path_info(path)
                if isinstance(res, dict):
                    self.speak(f"I've retrieved the metadata for {res['name']}. Its size is {res['size_human']}.")
                return res

        elif action == 'check_system_logs':
            logs = obj.get_recent_logs()
            if logs:
                return f"RECENT SYSTEM LOGS:\n{logs}"
            else:
                return "System logs are currently empty."

        elif action == 'execute_python':
            code = params.get('code')
            if code:
                from Leyncxity.features.code_executor import execute_python_code
                self.speak("Executing local automation script...")
                res = execute_python_code(code)
                return res

startExecution = MainThread()

class Main(QMainWindow):
    userInputSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.sendBtn.clicked.connect(self.handle_gui_input)
        self.ui.userInput.returnPressed.connect(self.handle_gui_input)
        
        startExecution.chatSignal.connect(self.update_chat)
        startExecution.statusSignal.connect(self.update_status)
        startExecution.speakingSignal.connect(self.ui.orb.setIntensity)
        startExecution.moodSignal.connect(self.ui.orb.setMood)
        self.userInputSignal.connect(startExecution.receive_input)

    def update_chat(self, text):
        self.ui.textBrowser_3.append(text)
        self.ui.textBrowser_3.ensureCursorVisible()

    def update_status(self, text):
        self.ui.status_label.setText(text)

    def receive_input(self, text):
        pass

    def handle_gui_input(self):
        text = self.ui.userInput.text()
        if text.strip():
            obj.stop_tts()
            self.ui.textBrowser_3.append(f"<b>USER:</b> {text}")
            self.ui.userInput.clear()
            startExecution.receive_input(text)
            if not startExecution.isRunning():
                startExecution.start()

    def startTask(self):
        if not startExecution.isRunning():
            startExecution.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    leyncxity = Main()
    leyncxity.show()
    sys.exit(app.exec_())
