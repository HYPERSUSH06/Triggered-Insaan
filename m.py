import socket
import keyboard
import time
import json
import threading
import sys
import win32api
import numpy as np
import cv2
from mss import mss as mss_module
from ctypes import WinDLL

class InteractionModule:
    def __init__(self):
        self.sct = mss_module()
        self.active_mode = False
        self.exit_program = False
        self.lock = threading.Lock()

        # Load configuration
        with open('config.json') as json_file:
            data = json.load(json_file)
        self.interaction_hotkey = int(data["interaction_hotkey"], 16)
        self.color_range = data["color_range"]
        self.R, self.G, self.B = data["target_color"]["R"], data["target_color"]["G"], data["target_color"]["B"]

        # Open socket connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 65432))

        user32 = WinDLL("user32")
        self.WIDTH, self.HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    def color_detection(self):
        img = np.array(self.sct.grab({'top': 0, 'left': 0, 'width': self.WIDTH, 'height': self.HEIGHT}))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Create a mask for the target color
        lower_bound = np.array([self.R - self.color_range, self.G - self.color_range, self.B - self.color_range])
        upper_bound = np.array([self.R + self.color_range, self.G + self.color_range, self.B + self.color_range])
        mask = cv2.inRange(img, lower_bound, upper_bound)

        if np.any(mask):
            self.sock.send(b'k')  # Trigger firing

    def hold_mode(self):
        while not self.exit_program:
            if win32api.GetAsyncKeyState(self.interaction_hotkey) < 0:
                self.active_mode = True
                self.color_detection()
            else:
                time.sleep(0.001)

    def start(self):
        threading.Thread(target=self.hold_mode).start()
        while not self.exit_program:
            if keyboard.is_pressed("ctrl+shift+x"):
                self.exit_program = True
                sys.exit()

if __name__ == "__main__":
    interaction_module = InteractionModule()
    interaction_module.start()
