import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from src.model import Detector
import time
from src.utils import call_police, turn_on_alarm

if __name__ == '__main__':
    app = Detector(mode = 'openai')

    while True:
        time.sleep(2)
        print("Starting...")
        human_result = app.analyzing_human_detection()
        if human_result.is_human:
            thief_result = app.analyzing_thief_detection()
            if thief_result.is_thief:
                print(turn_on_alarm())
                print(call_police())
                break
        
    
