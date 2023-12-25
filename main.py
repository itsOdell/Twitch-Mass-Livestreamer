import os
import sys
import time
from utils import choose_file, start_streaming, stop_streaming
from art import LOGO_ART, error_style, reset_style, input_style
from inquirer import Text, List, prompt


os.system("cls")
print(LOGO_ART)
ACCOUNTS_PATH = f"{os.getcwd()}/accounts.txt"
ACCOUNTS = []
error_sleep_time = 10


if os.path.exists(ACCOUNTS_PATH) is True and os.path.getsize(ACCOUNTS_PATH) > 0:
    with open(ACCOUNTS_PATH, "r") as file:
        ACCOUNTS = [line.rstrip() for line in file]
elif os.path.exists(ACCOUNTS_PATH) is False:
    print(error_style + f"{ACCOUNTS_PATH} file not detected, please create it and paste all your stream keys, each key on a new line" + reset_style)
    time.sleep(error_sleep_time)
    sys.exit(-1)
else:
    print(error_style + f"{ACCOUNTS_PATH} file is empty, please paste your livestream keys there, each key on a new line" + reset_style)
    time.sleep(error_sleep_time)
    sys.exit(-1)


file_to_stream = choose_file()
file_to_stream_name = os.path.basename(file_to_stream)


if file_to_stream == "":
    print(error_style + "Invalid option selected, please choose a valid option. Program exiting in 5 seconds..." + reset_style)
    time.sleep(5)
    sys.exit(-1)

questions = [List("gpu", message=input_style + "Select your GPU", choices=["None", "NVIDIA", "AMD"]),
            List("logging", message=input_style + "Do you want logging", choices=["Yes", "No"]), 
                List("quality", message=input_style + "Choose video quality", choices=["360", "480", "720", "1080"])]
answers = prompt(questions)

try:
    start_streaming(file_to_stream, ACCOUNTS, logging=answers["logging"], quality=answers["quality"], gpu=answers["gpu"])

    # input(light_magenta + f"{len(ACCOUNTS)} accounts have started streaming. Press 'Enter' to exit")
except KeyboardInterrupt:
    stop_streaming()
