import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from src.model import Detector
from src.utils import capture_screenshots

if __name__ == '__main__':
    output_folder = 'images'
    detector = Detector(mode='openai')
    user_input = int(input("Are you testing with: \n 1) local video\n 2) streaming camera\n"))
    if user_input == 1:
        video_path = 'video_testing.mov' 
        capture_screenshots(source=video_path, 
                            output_folder=output_folder, 
                            interval_seconds=2, 
                            streaming=False,
                            detector=detector)
    else:
        capture_screenshots(output_folder=output_folder, 
                            interval_seconds=2, 
                            streaming=True,
                            detector=detector)

        
    
