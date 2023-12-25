import sys
import os
import subprocess
import time
from tkinter import filedialog, Tk
from art import input_style, success_style, light_magenta, reset_style, error_style

ALLOWED_TYPES = "*.mp4 *.png *.gif"
IS_LIVE_CURRENTLY = False
STOPPED_STREAMING = True
CONFIGS = {
    "360": {
     "resolution": "640x360",
     "bitrate": "400k -maxrate 400k -bufsize 800k"
    },
    "480": {
     "resolution": "854x480",
     "bitrate": "2000k -maxrate 2000k -bufsize 4000k"
    },
    "720": {
     "resolution": "1280x720",
     "bitrate": "4000k -maxrate 4000k -bufsize 8000k"
    },
    "1080": {
     "resolution": "1920x1080",
     "bitrate": "6000k -maxrate 6000k -bufsize 12000k"
    }
}

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


def start_streaming(file, stream_keys, quality, logging):
    global IS_LIVE_CURRENTLY, STOPPED_STREAMING
    STOPPED_STREAMING = False
    if not STOPPED_STREAMING:   
        try:
            command = (
                f'{resource_path("ffmpeg.exe")} -stream_loop -1 -re -i "{file}" -map 0:v '
                f'-s {CONFIGS[quality]["resolution"]} -profile:v baseline -tune zerolatency '
                f'-c:v libx264 -preset ultrafast -b:v {CONFIGS[quality]["bitrate"]} '
                f'-pix_fmt yuv420p -g 50 -c:a aac -b:a 128k -ar 44100 '
                f'-flags +global_header -f tee "'
            )
            for key in stream_keys:
                command += f"[select=\\'v:0,a:0\\':f=flv]rtmp://live.twitch.tv/app/{key}|"
            command = command[:-1] + '"'
            IS_LIVE_CURRENTLY = True
            print(success_style + f"{len(stream_keys)} accounts have successfully started streaming!")
            print(light_magenta + "Press 'CTRL + C' to exit")
            if logging == "Yes":
                subprocess.run(command, check=True)
            else:
                subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
        except subprocess.CalledProcessError as e:
            if not STOPPED_STREAMING and IS_LIVE_CURRENTLY:
                print(error_style + "Attempting to restart the stream...")
                return start_streaming(file, stream_keys, quality)

    
def stop_streaming():
    try:
        global IS_LIVE_CURRENTLY, STOPPED_STREAMING
        IS_LIVE_CURRENTLY = False
        STOPPED_STREAMING = True
        subprocess.run("taskkill /f /im ffmpeg.exe")
        print(success_style + "Successfully killed streamer!")
        input(light_magenta + "Press 'Enter' to exit out ")
        sys.exit(0)
    except Exception:
        print(error_style + "There was an error trying to kill the streamer")