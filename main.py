from model import Detector
import time

app = Detector(mode = 'openai')

while True:
    time.sleep(2)
    result = app.analyzing_human_detection()
    if result.is_human:
        app.analyzing_thief_detection()
    
