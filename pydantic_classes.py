from langchain_core.pydantic_v1 import BaseModel, Field


class ThiefDetector(BaseModel):
    is_thief: bool = Field(..., description = 'It defines if there are someone entering in the property with bad intensions')

class HumanDetector(BaseModel):
    is_human: bool = Field(..., description = 'It defines if there is someone in the frame')

