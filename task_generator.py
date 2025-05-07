import json
import datetime
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Use "gemini-pro" or "gemini-1.5-pro" if available
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

output_parser = StrOutputParser()

# Load user profile data
def load_user_profile():
    with open("user_profile.json", "r") as file:
        return json.load(file)

# Generate daily tasks using Gemini
def generate_tasks():
    profile = load_user_profile()
    today = datetime.date.today().strftime("%B %d, %Y")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a personal productivity coach who gives 1 focused task daily based on the user's life context. Give reply in a friendly and encouraging tone "),
        ("user", f"""Today is {today}.
Here is my profile:
Goal: {profile['goal']}
Current Skills: {profile['skills']}
Available Time Per Day: {profile['daily_time']}
Preferred Learning Style: {profile['learning_style']}
Motivation Level: {profile['motivation']}

Generate today's 1–3 tasks. Be specific and encouraging.""")
    ])

    chain = prompt | llm | output_parser
    return chain.invoke({})
