import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv
from src.pydantic_classes import HumanDetector, ThiefDetector, AllowedResolution
from src.utils import retrieve_current_image, retrieve_sequence_past_images, create_prompt_human_detector, create_prompt_thief_detector, call_police, turn_on_alarm
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.globals import set_debug
from langchain_core.runnables.base import RunnableParallel

set_debug(True)

load_dotenv()


class Detector:

    def __init__(self, model, resolution:AllowedResolution):
        self.model = model
        self.resolution = AllowedResolution(resolution = resolution)
        self.__creating_human_detection_chain()
        self.__creating_thief_detection_chain()
        self.__creating_main_chain()

    def __creating_human_detection_chain(self):
        self.human_detection_chain = create_prompt_human_detector | self.model.with_structured_output(HumanDetector)

    def analyzing_human_detection(self):
        return self.human_detection_chain.invoke({
                            'current_image':retrieve_current_image(self.resolution)
                            })
 
    def __creating_thief_detection_chain(self):
        self.thief_detection_chain = create_prompt_thief_detector \
                                        | self.model.with_structured_output(ThiefDetector)
                 
    def analyzing_thief_detection(self):
        return self.thief_detection_chain.invoke({ 
                            'sequence_images':retrieve_sequence_past_images(self.resolution)
                            })

    def __is_human_present_condition(self, output_human_detection_chain):
         """
         This function determinates if there are human/s in the image.
         If yes, it executes a chain which analyzes if the behaviour of people in the images is criminal or casual.
         """
         if output_human_detection_chain.is_human:
            return self.analyzing_thief_detection_chain
         else:
              return output_human_detection_chain

    def __analyzing_human_behaviour_condition(self, result):
        if type(result).__name__ == 'ThiefDetector':
            if result.is_thief == True:
                return self.thief_detected_chain
            else:
                return self.no_thief_detected_chain

        else:
            return self.no_human_detected_chain

    def __creating_main_chain(self):
        self.analyzing_thief_detection_chain = (lambda input: {'sequence_images':retrieve_sequence_past_images(self.resolution)}) | self.thief_detection_chain
        self.thief_detected_chain = RunnableParallel(
                    {'call_police':(lambda input: call_police(message = input.description)),
                     'turn_alarm': (lambda input: turn_on_alarm())
                    }) \
                    | RunnableLambda(lambda input: {'output': {'is_human': True, 'is_thief': True}})
                
        self.no_thief_detected_chain = RunnableLambda(lambda input: {'output': {'is_human': True, 'is_thief': False}})
        self.no_human_detected_chain = RunnableLambda(lambda input: {'output': {'is_human': False, 'is_thief': False}})

        self.chain = self.human_detection_chain \
                        | RunnableLambda(self.__is_human_present_condition) \
                        | RunnableLambda(self.__analyzing_human_behaviour_condition)


if __name__ == '__main__':
    from langchain_openai import ChatOpenAI

    model = ChatOpenAI(model="gpt-4o", 
                    temperature = 0)

    #model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
