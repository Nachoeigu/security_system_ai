import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from pydantic import BaseModel, Field
from typing import Literal


class ThiefDetector(BaseModel):
    is_thief: bool = Field(..., description = 'It defines if there are someone entering in the property with bad intensions')
    description: str = Field(..., description = 'If is_thief = False, return "". Otherwise, describe the sequence to report the police about the incident')

class HumanDetector(BaseModel):
    is_human: bool = Field(..., description = 'It defines if there is someone in the frame')

class ModelFunction(BaseModel):
    my_param: Literal['human_detector', 'thief_detector']

class AllowedResolution(BaseModel):
    resolution: Literal['high', 'low'] = Field(..., description = "The resolution of the provided images to the LLM")
