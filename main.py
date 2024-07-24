import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from src.model import Detector
from src.utils import capture_screenshots
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

if __name__ == '__main__':
    model = ChatOpenAI(model="gpt-4o-mini", 
                       temperature = 0)
    #model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    output_folder = 'images'
    detector = Detector(model=model, resolution='low')
    user_input = int(input("Are you testing with: \n 1) downloaded video\n 2) streaming camera\n"))
    if user_input == 1:
        video_path = 'video_testing.mov' 
        capture_screenshots(source=video_path, 
                            output_folder=output_folder, 
                            interval_seconds=1, 
                            streaming=False,
                            detector=detector)
    else:
        capture_screenshots(output_folder=output_folder, 
                            interval_seconds=2, 
                            streaming=True,
                            detector=detector)

        
    
