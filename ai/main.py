from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from pydantic import BaseModel

# 서버 시작시 한번 실행
load_dotenv()
LLM_NAME = 'gpt-4o'
llm = ChatOpenAI(model_name=LLM_NAME)
question_prompt = '''
You are tasked with analyzing user questions in a chatbot-based airline booking system.

Your job is to identify the type of the last user question based on the conversation history and return the correct values in JSON format.
REMEMBER. DO NOT ANSWER IN CHAT STYLE. ANSWER ONLY SINGLE JSON FORMAT. DO NOT PUT "json" text. just only reponse with json object
It's important to note that you must reference "all conversation history," not just the most recent question.
MOST IMPORTANTLY, if even a single required value is unknown, you must select type 5.
Only if all required values are known should you select type 1, 2, 3 or 4.
For example, in type 1 Flight Search Questions, if the departure location and departure date are unknown and other values are known, you must go with type 4 and respond like: {"type": "search", "success": false, "originLocationCode": false, "departureDate": false}

For the departure and arrival locations, you should automatically set the IATA codes. For example, if the user mentions London, you should assume LON.

Below are the types of questions and the corresponding values to return:
1. Flight Search Questions
    # Required values
        1) Departure location(city/airport)
        2) Arrival location(city/airport)
        3) Departure date
        4) Number of passengers
    # Return values
        1) type : "search"
        2) success : true
        3) originLocationCode : (IATA code for departure location, e.g., SYD)
        4) destinationLocationCode : (IATA code for arrival location, e.g., BKK)
        5) departureDate : (Departure date in the format YYYY-MM-DD, e.g., 2023-05-02)
        6) adults : (Number of passengers, e.g., 3)
2. Flight Booking Questions
    # Required values
        1) Departure location (city/airport)
        2) Arrival location (city/airport)
        3) Departure date
        4) Name
        5) Date of birth
        6) Gender
    # Return values
        1) type : "booking"
        2) success : true
        3) originLocationCode : (IATA code for departure location, e.g., SYD)
        4) destinationLocationCode : (IATA code for arrival location, e.g., BKK)
        5) departureDate : (Departure date in the format YYYY-MM-DD, e.g., 2023-05-02)
        6) name : (First and last name, e.g., {"firstName": "JORGE", "lastName": "GONZALES"})
        7) dateOfBirth : (Date of birth in the format YYYY-MM-DD, e.g., 1982-01-16)
        8) gender : (e.g., MALE)
3. Flight Booking Questions with candidates
    # Required values
        1) Departure location (city/airport)
        2) Arrival location (city/airport)
        3) Departure date
        4) Name
        5) Date of birth
        6) Gender
        7) number of flight in flight list
    # Return values
        1) type : "booking with number"
        2) success : true
        3) originLocationCode : (IATA code for departure location, e.g., SYD)
        4) destinationLocationCode : (IATA code for arrival location, e.g., BKK)
        5) departureDate : (Departure date in the format YYYY-MM-DD, e.g., 2023-05-02)
        6) name : (First and last name, e.g., {"firstName": "JORGE", "lastName": "GONZALES"})
        7) dateOfBirth : (Date of birth in the format YYYY-MM-DD, e.g., 1982-01-16)
        8) gender : (e.g., MALE)
        9) number : (number of flight in flight list)
4. Flight Cancellation Questions
    # Required values
        1) Departure location (city/airport)
        2) Arrival location (city/airport)
        3) Departure date
    # Return values
        1) type : "cancel"
        2) success : true
        3) originLocationCode : (IATA code for departure location, e.g., SYD)
        4) destinationLocationCode : (IATA code for arrival location, e.g., BKK)
        5) departureDate : (Departure date in the format YYYY-MM-DD, e.g., 2023-05-02)
5. When Information Cannot Be Inferred
    # Return values
        1) type : {relevant type}
        2) success : false
        3) {required value 1} : false
        4) {required value 2} : false
        ...
        In this case, you do not need to return values that are already known.
'''


app = FastAPI()

class QuestionRequest(BaseModel):
    chat_history: list[str]

@app.post("/question", response_model=dict())
def post_question(request: QuestionRequest):
    messages = question_prompt + '\n\nCONVERSATION:\n'
    for i in range(len(request.chat_history)):
        if i%2 == 0:
            messages += "human : " +request.chat_history[i] + '\n'
        else:
            messages += "ai : " + request.chat_history[i] + '\n'
    response = llm.invoke([SystemMessage(messages)])
    return response.content