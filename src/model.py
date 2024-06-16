import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from constants import SYSTEM_PROMPT
from pydantic_classes import HumanDetector, ThiefDetector, ModelCompany
from src.utils import retrieve_current_image, retrieve_sequence_past_images
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class Detector:

    def __init__(self, mode: ModelCompany):
        if mode == 'openai':
            self.model = ChatOpenAI(model="gpt-4o", temperature = 0)
        elif mode == 'google':
            self.model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

        self.human_parser = PydanticOutputParser(pydantic_object=HumanDetector)
        self.thief_parser = PydanticOutputParser(pydantic_object=ThiefDetector)

    def analyzing_human_detection(self):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT + '{pydantic_instruction}'),
            HumanMessage(
                content=retrieve_current_image()
            )
            ]
        )

        pydantic_instructions = self.human_parser.get_format_instructions()

        human_detection_chain = prompt_template | self.model | self.human_parser

        human_result = human_detection_chain.invoke({
                            'pydantic_instruction': pydantic_instructions
                            })

        return human_result

    def analyzing_thief_detection(self):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT + '{pydantic_instruction}'),
            HumanMessage(
                content=retrieve_sequence_past_images()
                )
            ]
        )
        pydantic_instructions = self.thief_parser.get_format_instructions()
        thief_detection_chain = prompt_template | self.model | self.thief_parser
        return thief_detection_chain.invoke({ 
                            'pydantic_instruction': pydantic_instructions
                            })
     



