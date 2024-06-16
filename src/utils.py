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
    path_last_shot = sorted(Path(f'{WORKDIR}/images').glob('*.jpg'), key=lambda x: int(x.stem), reverse=True)[0]
    past_last_shot = '/'.join(path_last_shot.parts)[1:]
    output =  [{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{encoding_img(past_last_shot)}"}}]
    return output

def turn_on_alarm():
    return "Alarm Turned On"

def call_police():
    return "Police notified"

def retrieve_sequence_past_images():
    images = sorted(Path(f"{WORKDIR}/images").glob('*.jpg'), key=lambda x: int(x.stem), reverse=True)[:4]
    output = [{"type":"text","text":"Make your analysis based on this sequence of images"}]

    for image in images:
        image_path = '/'.join(image.parts)[1:]
        output.append({"type": "image_url", "image_url":{"url":f"data:image/jpg;base64,{encoding_img(image_path)}"}})

    return output