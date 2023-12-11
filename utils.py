import sys
import os
import subprocess
import time
from tkinter import filedialog, Tk
from art import input_style, success_style, light_magenta, reset_style

ALLOWED_TYPES = "*.mp4 *.png *.gif"

def resource_path(another_way):
    try:
        usual_way = sys._MEIPASS
    except Exception:
        usual_way = os.path.dirname(__file__)
    return os.path.join(usual_way, another_way)

def choose_file():
    print(input_style + "Please enter a file to stream (allowed formats: mp4, png, gif): " + reset_style)
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=f"Select a file to stream", filetypes=[("Video/Image Files", ALLOWED_TYPES)])
    root.destroy()

    return file_path


def start_streaming(file, stream_key):
    command = (
        f'{resource_path("ffmpeg.exe")} -stream_loop -1 -re -i "{file}" '
        f'-c:v libx264 -preset veryfast -b:v 3000k -maxrate 3000k -bufsize 6000k '
        f'-pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ar 44100 '
        f'-f flv "rtmp://live.twitch.tv/app/{stream_key}"'
    )
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(success_style + "Livestream has started!" + reset_style)


def handle_exit():
    print(light_magenta + "Exiting..." + reset_style)
    subprocess.run(['taskkill', '/f', '/im', 'ffmpeg.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(success_style + "All livestreams have closed. Program exiting in 10 seconds" + reset_style)
    time.sleep(10)
    sys.exit(0)