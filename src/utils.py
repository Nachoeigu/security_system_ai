import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

import base64
from pathlib import Path
from langchain.tools import tool
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from src.model import Detector

from langchain_core.messages import HumanMessage, SystemMessage
from constants import SYSTEM_PROMPT_FOR_HUMAN_DETECTION, SYSTEM_PROMPT_FOR_THIEF_DETECTION
import cv2
import time

def analyzing_image(detector) -> bool:
    return detector.chain.invoke({
        'pydantic_instruction': detector.human_parser_instructions,
        'current_image':retrieve_current_image(detector.resolution)
        })


def checking_if_directory_exist(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def opening_video(streaming, source):
    if streaming:
        cap = cv2.VideoCapture(0)  # Open the default camera
    else:
        cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        raise Exception(f"Unable to open video source {source}")

    return cap

def capture_screenshots(detector:'Detector', source:str='', output_folder:str='images', interval_seconds:int=3, streaming:bool=False):
    checking_if_directory_exist(output_folder=output_folder)
    cap = opening_video(streaming=streaming, source=source)

    screenshots = []
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            if not streaming:
                break
            else:
                continue

        current_time = time.time()
        elapsed_time = current_time - start_time

        # Capture a frame every interval_seconds
        if elapsed_time >= interval_seconds:
            current_timestamp = int(current_time)  # Use current_time instead of time.time()
            image_path = os.path.join(output_folder, f"{current_timestamp}.jpg")
            cv2.imwrite(image_path, frame)
            screenshots.append(image_path)
            
            if streaming:
                video_time_sec = elapsed_time
            else:
                video_time_msec = cap.get(cv2.CAP_PROP_POS_MSEC)
                video_time_sec = video_time_msec / 1000

            minutes = int(video_time_sec // 60)
            seconds = int(video_time_sec % 60)
            print("Analyzing if there is a human in the screenshot")

            result_of_analysis = analyzing_image(detector)
            if result_of_analysis['output']['is_thief']:
                print(f"The moment when it was detected was {minutes} minute(s) and {seconds} second(s)")
                break

            start_time = time.time()  # Reset start time after analysis

            # Keep only the last 4 screenshots
            if len(screenshots) > 4:
                oldest_screenshot = screenshots.pop(0)
                if os.path.exists(oldest_screenshot):
                    os.remove(oldest_screenshot)

        # Sleep for a short duration to prevent high CPU usage
        time.sleep(0.01)

    cap.release()


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

def retrieve_current_image(resolution:str):
    path_last_shot = sorted(Path(f'{WORKDIR}/images').glob('*.jpg'), key=lambda x: int(x.stem), reverse=True)[0]
    past_last_shot = '/'.join(path_last_shot.parts)[1:]
    output =  [{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{encoding_img(past_last_shot)}", "details": f"{resolution}"}}]
    return output

def turn_on_alarm():
    return "Alarm Turned On"

def call_police(message:str) -> str:
    return f"Police notified with the following description:\n{message}"


def retrieve_sequence_past_images(resolution:str):
    images = sorted(Path(f"{WORKDIR}/images").glob('*.jpg'), key=lambda x: int(x.stem), reverse=True)[:4]
    output = [{"type":"text","text":"Make your analysis based on this sequence of images"}]

    for image in images:
        image_path = '/'.join(image.parts)[1:]
        output.append({"type": "image_url", "image_url":{"url":f"data:image/jpg;base64,{encoding_img(image_path)}", "details": f"{resolution}"}})

    return output

@tool
def create_prompt_human_detector(pydantic_instruction:str, current_image:List[Dict]):
    """
    This function creates the prompt with two inputs parameters:
    - pydantic_instruction: How the LLM should structure the output
    - current_image: A formated list so the LLM can read the image
    """
    return  [
        SystemMessage(
            content = SYSTEM_PROMPT_FOR_HUMAN_DETECTION + f"{pydantic_instruction}"
        ),
        HumanMessage(
            content=current_image
        )
    ]

@tool
def create_prompt_thief_detector(pydantic_instruction:str, sequence_images:List[Dict]):
    """
    This function creates the prompt with two inputs parameters:
    - pydantic_instruction: How the LLM should structure the output
    - sequence_images: A formated list so the LLM can read the sequence of images
    """
    return  [
        SystemMessage(
            content = SYSTEM_PROMPT_FOR_THIEF_DETECTION + f"{pydantic_instruction}"
        ),
        HumanMessage(
            content=sequence_images
        )
    ]

