# Prototype Code

import pyaudio
import signal

import numpy as np
from scipy.fft import fft

import vgamepad as vg



class Grabadora():
    def __init__(self):
        self.grabando = False
        signal.signal(signal.SIGINT, 
            self.signal_handler)
        self.gamepad = vg.VX360Gamepad()

        self.keys = {
            "left": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            "right": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
            "up": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            "down": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            "a":vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
            "b":vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
            "select":vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            "start":vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
        }

    def signal_handler(self, sig, 
    frame):
        print('Finalizando')
        self.grabando = False

    def esta_grabando(self):
        return self.grabando

    def send_key(self, key, update=True):
        if key == "reset":
            self.gamepad.reset()
            if update:
                self.gamepad.update()
            return None
        else:
            self.gamepad.press_button(button=self.keys[key])  # press the A button
            self.gamepad.update()
            return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT

    def iniciar(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        CHUNK = 1024
        WAVE_OUTPUT_FILENAME = \
        "output.wav"

        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        self.grabando = True

        print("Grabando")

        lastKey = 0
        lastKeyCommand = None
        idle_ticks = 0
        while self.esta_grabando():
            data = stream.read(CHUNK)
            frames = data
            data_np = np.frombuffer(data, dtype=np.int16)
            freqs = fft(data_np)
            frequencies = np.fft.fftfreq(len(freqs), 1/RATE)
            amplitudes = np.abs(freqs)
            index_of_max_amplitude = np.argmax(amplitudes)
            dominant_frequency = frequencies[index_of_max_amplitude]
            if(dominant_frequency == 0 or ( 40 <= dominant_frequency <= 50)):
                idle_ticks +=1
                if(idle_ticks >= 10):
                    idle_ticks = 0
                    lastKeyCommand = self.send_key("reset")
            else:
                    lastKeyCommand = None
                    lastKeyCommand = self.send_key("reset")
                    
                    if(946 <= dominant_frequency <= 948):
                        if  1936 <= lastKey <= 1938:
                            lastKeyCommand = self.send_key("b")
                        else:
                            print("A + Left")
                            lastKeyCommand = self.send_key("left", update=False)
                            lastKeyCommand = self.send_key("a")
                    if(2539 <= dominant_frequency <= 2541):
                        print("B + Left")
                        lastKeyCommand = self.send_key("left", update=False)
                        lastKeyCommand = self.send_key("b")
                    if(2195 <= dominant_frequency <= 2197):
                        print("B + Right")
                        lastKeyCommand = self.send_key("right", update=False)
                        lastKeyCommand = self.send_key("b")
                    if(860 <= dominant_frequency <= 862):
                        print("A + Right")
                        lastKeyCommand = self.send_key("right", update=False)
                        lastKeyCommand = self.send_key("a")
                    if(1161 <= dominant_frequency <= 1163):
                        print("Left")
                        lastKeyCommand = self.send_key("left")
                    if(688 <= dominant_frequency <= 690 ):
                        print("Up")
                        lastKeyCommand = self.send_key("up")
                    if(558 <= dominant_frequency <= 560):
                        print("Right")
                        lastKeyCommand = self.send_key("right")
                    if(1032 <= dominant_frequency <= 1034):
                        lastKeyCommand = self.send_key("down")
                        print("Down")
                    if(774 <= dominant_frequency <= 776):
                        lastKeyCommand = self.send_key("a")
                        print("a")
                    if(1936 <= dominant_frequency <= 1938):
                        lastKeyCommand = self.send_key("b")
                        print("b")
                    if(1 <= dominant_frequency <= 1):
                        lastKeyCommand = self.send_key("start")
                        print("start")
                    if(515 <= dominant_frequency <= 517):
                        lastKeyCommand = self.send_key("select")
                        print("select")

                    if(lastKeyCommand == None):
                        print("Frecuencia dominante:", dominant_frequency, "Hz")
                        lastKeyCommand = self.send_key("reset")
                    pass
                

                    lastKey = dominant_frequency

        
        print("Terminada!")

        stream.stop_stream()
        stream.close()
        audio.terminate()

grabadora = Grabadora()
grabadora.iniciar()