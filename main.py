import os
import sys
import time
from utils import choose_file, start_streaming, handle_exit
from art import LOGO_ART, error_style, light_magenta, reset_style


os.system("cls")
print(LOGO_ART)
KEYS_PATH = f"{os.getcwd()}\\keys.txt"
ACCOUNTS = []
error_sleep_time = 10


if os.path.exists(KEYS_PATH) is True and os.path.getsize(KEYS_PATH) > 0:
    with open(KEYS_PATH, "r") as file:
        ACCOUNTS = file.readlines()
elif os.path.exists(KEYS_PATH) is False:
    print(error_style + f"{KEYS_PATH} file not detected, please create it and paste all your stream keys, each key on a new line" + reset_style)
    time.sleep(error_sleep_time)
    sys.exit(-1)
else:
    print(error_style + f"{KEYS_PATH} file is empty, please paste your livestream keys there, each key on a new line" + reset_style)
    time.sleep(error_sleep_time)
    sys.exit(-1)


file_to_stream = choose_file()
file_to_stream_name = os.path.basename(file_to_stream)

if file_to_stream == "":
    print(error_style + "Invalid option selected, please choose a valid option. Program exiting in 5 seconds..." + reset_style)
    time.sleep(5)
    sys.exit(-1)

for account in ACCOUNTS:
    start_streaming(file_to_stream, account)

input(light_magenta + f"{len(ACCOUNTS)} accounts have started streaming. Press 'Enter' to exit")

handle_exit()
