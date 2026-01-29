# Developed by Leyn.cx
from PyQt5 import QtCore, QtGui, QtWidgets
import math
import psutil
try:
    import GPUtil
except ImportError:
    GPUtil = None

class SystemVitalsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(900, 500)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.update_stats)
        self._timer.start(1000) 
        
        self.stats = {
            "cpu": 0,
            "ram": 0,
            "gpu": 0,
            "net_down": 0,
            "net_up": 0,
            "gpu_temp": 0
        }
        self.history = {"cpu": [0]*20, "ram": [0]*20}
        self.prev_net = psutil.net_io_counters()

    def update_stats(self):
        self.stats["cpu"] = psutil.cpu_percent()
        self.stats["ram"] = psutil.virtual_memory().percent
        
        self.history["cpu"].pop(0)
        self.history["cpu"].append(self.stats["cpu"])
        self.history["ram"].pop(0)
        self.history["ram"].append(self.stats["ram"])
        
        curr_net = psutil.net_io_counters()
        self.stats["net_down"] = (curr_net.bytes_recv - self.prev_net.bytes_recv) / 1024 
        self.stats["net_up"] = (curr_net.bytes_sent - self.prev_net.bytes_sent) / 1024
        self.prev_net = curr_net
        
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    self.stats["gpu"] = gpus[0].load * 100
                    self.stats["gpu_temp"] = gpus[0].temperature
            except:
                pass
        
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        accent = QtGui.QColor(139, 92, 246, 120) 
        
        painter.setPen(QtGui.QPen(accent, 1))
        # Top-Left Corner
        painter.drawLine(QtCore.QPoint(20, 20), QtCore.QPoint(100, 20))
        painter.drawLine(QtCore.QPoint(20, 20), QtCore.QPoint(20, 60))
        # Top-Right
        painter.drawLine(QtCore.QPoint(w-20, 20), QtCore.QPoint(w-100, 20))
        painter.drawLine(QtCore.QPoint(w-20, 20), QtCore.QPoint(w-20, 60))
        # Bottom-Left
        painter.drawLine(QtCore.QPoint(20, h-100), QtCore.QPoint(100, h-100))
        painter.drawLine(QtCore.QPoint(20, h-100), QtCore.QPoint(20, h-140))
        # Bottom-Right
        painter.drawLine(QtCore.QPoint(w-20, h-100), QtCore.QPoint(w-100, h-100))
        painter.drawLine(QtCore.QPoint(w-20, h-100), QtCore.QPoint(w-20, h-140))

        font = QtGui.QFont("Consolas", 8)
        painter.setFont(font)
        
        # 1. CPU
        self.draw_stat_box(painter, 40, 40, "CPU PROCESSOR", f"{self.stats['cpu']}%", self.history["cpu"], accent)
        
        # 2. RAM
        self.draw_stat_box(painter, w-220, 40, "MEMORY LOAD", f"{self.stats['ram']}%", self.history["ram"], accent)
        
        # 3. NETWORK
        self.draw_net_box(painter, 40, h-180, accent)
        
        # 4. GPU / SYSTEM
        gpu_label = "GPU CORE" if self.stats["gpu"] > 0 else "SYSTEM CORE"
        gpu_val = f"{int(self.stats['gpu'])}% | {int(self.stats['gpu_temp'])}°C" if self.stats["gpu"] > 0 else "STABLE"
        self.draw_simple_stat(painter, w-220, h-180, gpu_label, gpu_val, accent)

    def draw_stat_box(self, painter, x, y, label, value, history, color):
        painter.setPen(color)
        painter.drawText(x, y, label)
        painter.setPen(QtCore.Qt.white)
        painter.drawText(x, y + 20, value)
        
        painter.setPen(QtGui.QPen(color, 1))
        for i in range(len(history)-1):
            h1 = int(history[i] / 5)
            h2 = int(history[i+1] / 5)
            painter.drawLine(QtCore.QPoint(int(x + i*5), int(y + 50 - h1)), 
                             QtCore.QPoint(int(x + (i+1)*5), int(y + 50 - h2)))

    def draw_net_box(self, painter, x, y, color):
        painter.setPen(color)
        painter.drawText(x, y, "NETWORK TRAFFIC")
        painter.setPen(QtCore.Qt.white)
        painter.drawText(x, y+20, f"DWN: {self.stats['net_down']:.1f} KB/s")
        painter.drawText(x, y+35, f"UP:  {self.stats['net_up']:.1f} KB/s")

    def draw_simple_stat(self, painter, x, y, label, value, color):
        painter.setPen(color)
        painter.drawText(x, y, label)
        painter.setPen(QtCore.Qt.white)
        painter.drawText(x, y+20, value)

class OrbWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 400)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(16) 
        self._phase = 0
        self.is_talking = False
        self.current_mood = "idle" 
        self.mood_colors = {
            "idle": QtGui.QColor(139, 92, 246),      
            "thinking": QtGui.QColor(245, 158, 11),  
            "success": QtGui.QColor(16, 185, 129),   
            "error": QtGui.QColor(239, 68, 68),      
            "listening": QtGui.QColor(59, 130, 246)  
        }
        self.accent_color = self.mood_colors["idle"]
        self.electron_color = QtGui.QColor(192, 132, 252)

    def setIntensity(self, talking):
        self.is_talking = talking

    def setMood(self, mood):
        if mood in self.mood_colors:
            self.current_mood = mood
            self.accent_color = self.mood_colors[mood]

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        width, height = self.width(), self.height()
        center = QtCore.QPointF(width / 2, height / 2)
        
        self._phase += 0.05 if self.is_talking else 0.03
        
        nucleus_r = 35 + (math.sin(self._phase * 2) * (12 if self.is_talking else 4))
        
        grad = QtGui.QRadialGradient(center, nucleus_r * 2.5)
        color = self.accent_color
        grad.setColorAt(0, QtGui.QColor(color.red(), color.green(), color.blue(), 150 if self.is_talking else 60))
        grad.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        
        painter.setBrush(grad)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(center, nucleus_r * 2.0, nucleus_r * 2.0)
        
        painter.setBrush(self.accent_color)
        painter.drawEllipse(center, nucleus_r * 0.5, nucleus_r * 0.5)

        orbit_rx, orbit_ry = 180, 50
        orbit_count = 6
        
        for i in range(orbit_count):
            painter.save()
            painter.translate(center)
            painter.rotate(i * (180 / orbit_count))
            
            orbit_pen_color = QtGui.QColor(color.red(), color.green(), color.blue(), 50)
            painter.setPen(QtGui.QPen(orbit_pen_color, 1))
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawEllipse(QtCore.QPointF(0, 0), orbit_rx, orbit_ry)
            
            for j in range(2):
                e_angle = self._phase * (1.2 + i * 0.1) + (j * math.pi)
                ex, ey = orbit_rx * math.cos(e_angle), orbit_ry * math.sin(e_angle)
                e_center = QtCore.QPointF(ex, ey)
                e_grad = QtGui.QRadialGradient(e_center, 12)
                e_grad.setColorAt(0, QtGui.QColor(192, 132, 252, 180))
                e_grad.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
                painter.setBrush(e_grad)
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawEllipse(e_center, 9, 9)
                painter.setBrush(self.electron_color)
                painter.drawEllipse(e_center, 3, 3)
            painter.restore()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Leyncxity AI")
        MainWindow.resize(1200, 900)
        
        MainWindow.setStyleSheet(\
            "QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0F021A, stop:1 #000000); }")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(40, 20, 40, 30)
        self.main_layout.setSpacing(0)
        
        self.header = QtWidgets.QHBoxLayout()
        self.brand_info = QtWidgets.QVBoxLayout()
        self.brand_label = QtWidgets.QLabel("LEYNCXITY")
        self.brand_label.setStyleSheet("color: white; font: 24pt 'Segoe UI Light'; letter-spacing: 12px; font-weight: 100; background: transparent;")
        self.brand_info.addWidget(self.brand_label)
        
        self.status_label = QtWidgets.QLabel("SYSTEM MAINFRAME : ENGAGED")
        self.status_label.setStyleSheet("color: #8B5CF6; font: 7pt 'Consolas'; letter-spacing: 4px; background: transparent;")
        self.brand_info.addWidget(self.status_label)
        self.header.addLayout(self.brand_info)
        
        self.header.addStretch()
        
        self.ctrl_layout = QtWidgets.QHBoxLayout()
        self.pushButton = QtWidgets.QPushButton("WAKE")
        self.pushButton.setFixedSize(80, 32)
        self.pushButton.setStyleSheet("QPushButton { background-color: #1A0B3B; color: #C084FC; border: 1px solid #4C1D95; border-radius: 16px; font: bold 8pt 'Segoe UI'; } QPushButton:hover { background-color: #2E1065; }")
        self.ctrl_layout.addWidget(self.pushButton)
        
        self.pushButton_2 = QtWidgets.QPushButton("SLEEP")
        self.pushButton_2.setFixedSize(80, 32)
        self.pushButton_2.setStyleSheet("QPushButton { background-color: transparent; color: #F87171; border: 1px solid #7F1D1D; border-radius: 16px; font: bold 8pt 'Segoe UI'; } QPushButton:hover { background-color: rgba(127, 29, 29, 20); }")
        self.ctrl_layout.addWidget(self.pushButton_2)
        self.header.addLayout(self.ctrl_layout)
        self.main_layout.addLayout(self.header)
        
        self.main_layout.addStretch(1)
        
        self.center_frame = QtWidgets.QFrame()
        self.center_frame.setMinimumHeight(550)
        self.center_layout = QtWidgets.QStackedLayout(self.center_frame)
        
        self.vitals = SystemVitalsWidget()
        self.center_layout.addWidget(self.vitals)
        
        self.orb_container = QtWidgets.QWidget()
        self.orb_vbox = QtWidgets.QVBoxLayout(self.orb_container)
        self.orb = OrbWidget()
        self.orb_vbox.addWidget(self.orb, 0, QtCore.Qt.AlignCenter)
        
        self.sub_orb_label = QtWidgets.QLabel("NEURAL HARMONIC OSCILLATION : STABLE")
        self.sub_orb_label.setStyleSheet("color: rgba(139, 92, 246, 0.4); font: 8pt 'Segoe UI Light'; letter-spacing: 10px; background: transparent;")
        self.sub_orb_label.setAlignment(QtCore.Qt.AlignCenter)
        self.orb_vbox.addWidget(self.sub_orb_label)
        
        self.center_layout.addWidget(self.orb_container)
        self.center_layout.setStackingMode(QtWidgets.QStackedLayout.StackAll)
        
        self.main_layout.addWidget(self.center_frame)
        
        self.main_layout.addStretch(1)
        
        self.interaction_container = QtWidgets.QVBoxLayout()
        self.interaction_container.setSpacing(20)
        
        self.textBrowser_3 = QtWidgets.QTextBrowser()
        self.textBrowser_3.setFixedHeight(180)
        self.textBrowser_3.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); border: 1px solid #1E0E45; border-radius: 20px; color: #D1D5DB; padding: 15px; font: 10pt 'Segoe UI';")
        self.interaction_container.addWidget(self.textBrowser_3)
        
        self.input_pill = QtWidgets.QFrame()
        self.input_pill.setFixedHeight(60)
        self.input_pill.setFixedWidth(850)
        self.input_pill.setStyleSheet("background-color: #0F021A; border: 1px solid #2E1065; border-radius: 30px;")
        self.pill_layout = QtWidgets.QHBoxLayout(self.input_pill)
        self.pill_layout.setContentsMargins(25, 5, 10, 5)
        
        self.userInput = QtWidgets.QLineEdit()
        self.userInput.setPlaceholderText("Direct override command...")
        self.userInput.setStyleSheet("background: transparent; border: none; color: white; font: 11pt 'Segoe UI';")
        self.pill_layout.addWidget(self.userInput)
        
        self.sendBtn = QtWidgets.QPushButton("↑")
        self.sendBtn.setFixedSize(40, 40)
        self.sendBtn.setStyleSheet("QPushButton { background-color: #8B5CF6; color: white; border-radius: 20px; font: bold 16pt 'Segoe UI'; } QPushButton:hover { background-color: #7C3AED; }")
        self.pill_layout.addWidget(self.sendBtn)
        
        self.input_center_layout = QtWidgets.QHBoxLayout()
        self.input_center_layout.addWidget(self.input_pill, 0, QtCore.Qt.AlignCenter)
        self.interaction_container.addLayout(self.input_center_layout)
        
        self.main_layout.addLayout(self.interaction_container)
        
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
