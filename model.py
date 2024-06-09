from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages.human import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from constants import SYSTEM_PROMPT
from pydantic_classes import HumanDetector, ThiefDetector
from utils import retrieve_current_image, retrieve_sequence_images


load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature = 0)

human_prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT + '{pydantic_instruction}'),
    HumanMessage(
        content=retrieve_current_image()
    )
    ]
)
thief_prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT + '{pydantic_instruction}'),
    HumanMessage(
        content=retrieve_sequence_images()
        )
    ]
)


parser = PydanticOutputParser(pydantic_object=HumanDetector)
pydantic_instructions = parser.get_format_instructions()
human_detection_chain = human_prompt_template | model | parser

human_result = human_detection_chain.invoke({
                    'pydantic_instruction': pydantic_instructions
                    })

if human_result.is_human:
    parser = PydanticOutputParser(pydantic_object=ThiefDetector)
    pydantic_instructions = parser.get_format_instructions()
    thief_detection_chain = thief_prompt_template | model | parser
    thief_result = thief_detection_chain.invoke({ 
                        'pydantic_instruction': pydantic_instructions
                        })
    
print(human_result)

print(thief_result)



