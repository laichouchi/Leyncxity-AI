import os
import ctypes
import pythoncom
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

def set_volume(level):
    """Set system volume (0-100)."""
    try:
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        # level is 0 to 100, pycaw uses 0.0 to 1.0
        volume.SetMasterVolumeLevelScalar(float(level) / 100, None)
        return True
    except Exception as e:
        print(f"Volume Error: {e}")
        return str(e)

def mute_system(mute=True):
    """Mute or unmute system."""
    try:
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        volume.SetMute(1 if mute else 0, None)
        return True
    except Exception as e:
        print(f"Mute Error: {e}")
        return str(e)

def set_brightness(level):
    """Set screen brightness (0-100)."""
    try:
        sbc.set_brightness(level)
        return True
    except Exception as e:
        return str(e)

def lock_pc():
    """Lock the Windows workstation."""
    try:
        ctypes.windll.user32.LockWorkStation()
        return True
    except Exception as e:
        return str(e)

def suspend_pc():
    """Put PC into sleep mode."""
    try:
        # 0: Sleep, 1: Hibernate, 0: Force
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return True
    except Exception as e:
        return str(e)
