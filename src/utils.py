import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

import base64
from pathlib import Path
import time

def get_timestamped_filename(original_filename: str) -> str:
    timestamp = int(time.time())
    ext = original_filename.split(".")[-1]
    return f"{timestamp}.{ext}"

def cleanup_old_files(directory: Path, max_files: int):
    files = sorted(directory.iterdir(), key=os.path.getmtime, reverse=True)
    for file in files[max_files:]:
        file.unlink()


def encoding_img(path):
    with open(path, 'rb') as image_file:
        image_data =  base64.b64encode(image_file.read()).decode('utf-8')

    return image_data

def retrieve_current_image():
    output =  [{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{encoding_img(f'{WORKDIR}/images/current_log.jpg')}"}}]
    return output

def turn_on_alarm():
    return "Alarm Turned On"

def call_police():
    return "Police notified"

def retrieve_sequence_past_images():
    images = ['current_log.jpg','historical_log_1.jpg','historical_log_2.jpg','historical_log_3.jpg']
    output = [{"type":"text","text":"Make your analysis based on this sequence of images."}]

    for image in images:
        output.append({"type": "image_url", "image_url":{"url":f"data:image/jpg;base64,{encoding_img(WORKDIR+'/images/'+image)}"}})

    return output