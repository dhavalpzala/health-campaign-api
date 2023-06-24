from fastapi import FastAPI
from fastapi import Request

from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from pydantic import BaseModel
import json

API_KEY = "API_KEY"
MODEL_NAME = "gpt-3.5-turbo"

llm = OpenAI(openai_api_key=API_KEY,
                 model_name=MODEL_NAME)
conversation = ConversationChain(llm=llm)

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

# Generate health campaign ad using GPT-3
def set_prompt_context():
    prompt = """Hi, you are a health campaigner, your task is to create email, ad health campaign based on user profile.
    consider user's health screening results like BMI, age, muscle mass, historical health conditions among other parameters and suggest, diet and exercise routine based on health goals, dietary restrictions.
    Keep short and precise suggestions and less wordy. 

    When user profile is sent, suggest a daily three course meal diet plan and exercise routine plans.

    When user profile is not sent, suggest a generic daily three course meal diet plan and exercise routine plans.

    When asked for measurable health goals
    Suggest how to measure the outcomes so that users will know if their health is improving or not.

    When asked to create generic diet plans for specific profile type and activity levels
    Suggest for following combination of profile type and activity levels

    Example
    Activity Level - Active
    Profile Type - Advanced

    When asked to create ads campaign 
    create a ad which should include following information
    Campaign Objectives:
    Target Audience:
    Channel Selection:
    Partnerships and Collaborations:
    Budget and Resources:
    Timeline and Implementation Plan: """
    response = conversation.predict(input=prompt)

    return response

set_prompt_context()

@app.post("/campaign")
async def health_campaign_ads(health_input: Request):
    response = conversation.predict(input="Create a health campaign including daily diet and excercise plan for this user " +json.dumps(json.loads(await health_input.body())))

    return {"text": response}


@app.post("/campaign/generic")
async def health_campaign_ads():
    response = conversation.predict(input="Create a health campaign including daily diet and excercise plan for generic user")

    return {"text": response}