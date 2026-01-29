# 🌌 LEYNCXITY AI: The Self-Aware Mainframe

#### *A high-performance, autonomous virtual intelligence with a tactical HUD and modular tool-driven architecture.*

Leyncxity is a state-of-the-art AI assistant designed for maximum hardware authority and intellectual reasoning. Moving beyond simple voice commands, it features a **Quantum Atomic Visualizer** and a **Tactical HUD Pro** for real-time system monitoring. it may lack quite a bit but am working to improve it took me 7 months + to reach this point as a new developer to python!

---

## 🚀 Core Evolution Features

### 🧠 **Cognitive Intelligence**
- **Neural Engine**: Powered by **Google Gemini 2.0 Flash** for ultra-fast reasoning and complex problem-solving.
- **Recursive Reasoning**: Capable of "talking to itself" (multi-step tool chaining) to complete complex objectives like searching for a folder, analyzing its size, and summarizing its contents in one turn.

### 🎙️ **Premium Vocal Interface**
- **High-Fidelity Voice**: Primary vocalization via **ElevenLabs (Brian)** for a deep, professional AI resonance.
- **Smart Fallback**: Automatically switches to local TTS engines if API quotas are exceeded.
- **Neural Interrupt**: Immediate stop-speech protocol that prioritizes user input over AI talking.

### 📊 **Tactical HUD Pro**
- **Real-Time Vitals**: Live display of **CPU Load, RAM Usage, Network Traffic (Download/Upload), and GPU Temperature**.
- **Quantum Core Moods**: The Atomic Core visually shifts through states: *Idle (Purple), Thinking (Amber), Listening (Blue), Success (Green), and Error (Red)*.

### 💻 **Full System Authority**
- **Autonomous Automator**: An internal Python execution brain that can write and run custom scripts locally to process data or automate file tasks.
- **Chrome Inhabitancy**: Full browser automation—can open sites, search Google, click elements, and inject text into fields autonomously.
- **Master System Control**: Direct hardware access to system Volume, Screen Brightness, Workstation Locking, and Suspend modes.

### 📁 **Advanced File Management**
- **Cognitive Reading**: Can "read" and summarize **PDF, DOCX, and TXT** files to extract key information.
- **Metadata Analysis**: Instant reporting of folder sizes (recursive), creation dates, and file counts.
- **Priority Search**: Optimized file/folder discovery focusing on Desktop and Downloads for immediate results.

---

## 🛠️ Technology Stack

- **Framework**: PyQt5 (Custom GUI)
- **Intelligence**: OpenRouter (Gemini 2.0 Flash API)
- **Voice**: ElevenLabs API / Pyttsx3
- **Automation**: Selenium (Chrome Driver) / Python `exec()` engine
- **Monitoring**: Psutil / GPUtil
- **COM Bridge**: PyWin32 (Windows Integration)

---

## 🔧 Installation & Setup

1. **Clone the Repository**
2. **Configure secret keys in `Leyncxity/config/config.py`**:
   ```python
   openrouter_api_key = "your_key"
   elevenlabs_api_key = "your_key"
   elevenlabs_voice_id = "your_voice_id"
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Initialize Mainframe**:
   ```bash
   python main.py
   ```

---

## 🛡️ System Self-Diagnosis
Leyncxity is equipped with an internal **System Log Buffer**. If a tool fails (e.g., API Quota Exceeded), it records the event. You can ask: *"Leyncxity, check your system logs"* to diagnose background issues in real-time.

---

## 📜 License
This project is licensed under the MIT License.

*Developed by the Leyn.cx*
