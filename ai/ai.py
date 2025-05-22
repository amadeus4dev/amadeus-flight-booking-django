from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
import json

load_dotenv()
LLM_NAME = 'gpt-3.5-turbo'
llm = ChatOpenAI(model_name=LLM_NAME)

class State(TypedDict):
    chat_history: list[str]
    type: str
    success: bool
    originLocationCode: str
    destinationLocationCode: str
    departureDate: str
    adults: str
    number: str

def append_chat_history(prompt, chat_history):
    for i in range(len(chat_history)):
        if i%2 == 0:
            prompt += "human : " +chat_history[i] + '\n'
        else:
            prompt += "chatbot : " + chat_history[i] + '\n'
    return prompt

def classify_type(state: State):
    prompt = '''
        You are tasked with analyzing user questions in a chatbot-based airline booking system.
        Your job is to identify the type of the last user question based on the conversation history.

        Below are the types of questions:
        "search": Flight Search Questions
        "booking with number": Flight Booking Questions with candidates
        "cancel": Flight Cancellation Questions
        "list": Flight Reservation List Questions
        
        Return only type name ex: search, booking with number, cancel, list

        Below are the chat_history:

    '''
    prompt = append_chat_history(prompt, state['chat_history'])
    response = llm.invoke([SystemMessage(prompt)])
    return {'type': response.content, 'chat_history': state['chat_history']}

def extract_search(state: State):
    prompt = '''
        You are tasked with analyzing user questions in a chatbot-based airline booking system.
        Your job is to extract the value from the conversation history.

        Below are the values:
        1. originLocationCode : (IATA code for departure location, e.g., SYD)
        2. destinationLocationCode : (IATA code for arrival location, e.g., BKK)
        3. departureDate : (Departure date in the format YYYY-MM-DD, e.g., 2023-05-02)
        4. adults : (Number of passengers, e.g., 3)
        
        Return in json form.
        ex: {"originLocationCode": "SYD", "destinationLocationCode": "BKK", "departureDate": "2023-05-02", "adults": 3}

        IMPORTANT: if you can not resolve value from the conversation history, then set 'false' value.
        ex: {"originLocationCode": "SYD", "destinationLocationCode": "BKK", "departureDate": "false", "adults": 3}

        Below are the chat_history:

    '''
    prompt = append_chat_history(prompt, state['chat_history'])
    response = llm.invoke([SystemMessage(prompt)])
    dic = json.loads(response.content)
    success = 'false' in dic.values()
    return {type: state['type'], 'success': not success} | dic

def extract_booking_with_number(state: State):
    prompt = '''
        You are tasked with analyzing user questions in a chatbot-based airline booking system.
        Your job is to extract the value from the conversation history.

        Below are the values:
        1. number : (number of flight in flight list)
        
        Return in json form.
        ex: {"number": 3}

        IMPORTANT: if you can not resolve value from the conversation history, then set 'false' value.
        ex: {"number": "false"}

        Below are the chat_history:

    '''
    prompt = append_chat_history(prompt, state['chat_history'])
    response = llm.invoke([SystemMessage(prompt)])
    dic = json.loads(response.content)
    success = 'false' in dic.values()
    return {type: state['type'], 'success': not success} | dic

def extract_for_cancel(state: State):
    prompt = '''
        You are tasked with analyzing user questions in a chatbot-based airline booking system.
        Your job is to extract the value from the conversation history.

        Below are the values:
        1. number : (number of flight in flight list)
        
        Return in json form.
        ex: {"number": 3}

        IMPORTANT: if you can not resolve value from the conversation history, then set 'false' value.
        ex: {"number": "false"}

        Below are the chat_history:

    '''
    prompt = append_chat_history(prompt, state['chat_history'])
    response = llm.invoke([SystemMessage(prompt)])
    dic = json.loads(response.content)
    success = 'false' in dic.values()
    return {type: state['type'], 'success': not success} | dic

def extract_for_list(state: State):
    return {type: state['type'], 'success': True}

def determine_extract_type(state: State):
    return state['type']

graph = StateGraph(State)

graph.add_node("classify_type", classify_type)
graph.add_node("extract_search", extract_search)
graph.add_node("extract_booking_with_number", extract_booking_with_number)
graph.add_node("extract_for_cancel", extract_for_cancel)
graph.add_node("extract_for_list", extract_for_list)

graph.add_edge(START, "classify_type")
graph.add_conditional_edges(
    "classify_type",
    determine_extract_type,
    {
        "search": "extract_search",
        "booking with number": "extract_booking_with_number",
        "cancel": "extract_for_cancel",
        "list": "extract_for_list"
    }
)
graph.add_edge("extract_search", END)
graph.add_edge("extract_booking_with_number", END)
graph.add_edge("extract_for_cancel", END)
graph.add_edge("extract_for_list", END)

app = graph.compile()

class llm:
    def invoke(self, chat_history):
        response = app.invoke({'chat_history': chat_history})

        ## TODO
        # 문자열 "false"를 False로 바꾸기.
        # 각 type에 맞게 다 리턴하기
        if response['type'] == 'search':
            return {'type': 'search', 'originLocationCode': response['originLocationCode'], 
                    'destinationLocationCode': response['destinationLocationCode']}
        elif response['type'] == 'booking with number':
            pass
        elif response['type'] == 'cancel':
            pass
        elif response['type'] == 'list':