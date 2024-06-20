import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
from src.pydantic_classes import HumanDetector, ThiefDetector, AllowedResolution
from src.utils import retrieve_current_image, retrieve_sequence_past_images, create_prompt_human_detector, create_prompt_thief_detector

load_dotenv()


class Detector:

    def __init__(self, model, resolution:AllowedResolution):
        self.model = model
        self.resolution = AllowedResolution(resolution = resolution)
        self.human_parser = PydanticOutputParser(pydantic_object=HumanDetector)
        self.thief_parser = PydanticOutputParser(pydantic_object=ThiefDetector)
        self.human_parser_instructions = self.human_parser.get_format_instructions()
        self.thief_parser_instructions = self.thief_parser.get_format_instructions()
        self.__creating_human_detection_chain()
        self.__creating_thief_detection_chain()

    def __creating_human_detection_chain(self):
        self.human_detection_chain = create_prompt_human_detector | self.model | self.human_parser

    def analyzing_human_detection(self):
        return self.human_detection_chain.invoke({
                            'pydantic_instruction': self.human_parser_instructions,
                            'current_image':retrieve_current_image(self.resolution)
                            })
 
    def __creating_thief_detection_chain(self):
        self.thief_detection_chain = create_prompt_thief_detector | self.model | self.thief_parser
         
    def analyzing_thief_detection(self):
        return self.thief_detection_chain.invoke({ 
                            'pydantic_instruction': self.thief_parser_instructions,
                            'sequence_images':retrieve_sequence_past_images(self.resolution)
                            })
     




