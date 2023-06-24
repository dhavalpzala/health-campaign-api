from fastapi import FastAPI

from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from pydantic import BaseModel


class HealthInput(BaseModel):
    user_profile: str
    age: int
    gender: str
    height: str
    weight: str
    bmi: str
    muscleMass: str
    water: str
    boneMass: str
    protein: str
    healthGoals: str
    dietaryRestrictions: str
    activityLevel: str
    profileType: str
    historicalHealthConditions: str
    healthScreeningResults: str


app = FastAPI()

API_KEY = ""
MODEL_NAME = "text-davinci-003"


def generate_prompts(health_input):
    # prompt = PromptTemplate(
    #     input_variables=[],
    #     template=text,
    # )

    return health_input.healthScreeningResults


# Generate health campaign ad using GPT-3
def generate_health_campaign_ad(health_input):
    # Create an instance of the OpenAI class, specifying the model to be used.
    llm = OpenAI(openai_api_key=API_KEY,
                 model_name=MODEL_NAME)

    conversation = ConversationChain(llm=llm)
    prompt = generate_prompts(health_input)
    response = conversation.predict(input=prompt)

    return response


@app.post("/")
def health_campaign_ads(health_input: HealthInput):
    response = generate_health_campaign_ad(health_input)

    return {"text": response}
