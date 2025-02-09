# # collecting the all the recent data regarding the question is given to the model then based on it response will be provided

import time
from googlesearch import search
import os
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables from the .env file.
env_vars = dotenv_values(os.path.join(os.getcwd(), ".env"))

# Retrieve environment variables for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Grog client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to perform Google search and format results with exponential backoff
def GoogleSearch(query):
    retries = 5  # Number of retries in case of rate limiting.
    delay = 2  # Initial delay in seconds.
    for attempt in range(retries):
        try:
            # Perform Google search and get the results
            results = list(search(query, num_results=5))  # Perform the search
            # Format the answer
            Answer = f"The search results for '{query}' are: \n[start]\n"
            for i in results:
                Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
            Answer += "[end]"
            return Answer
        
        except Exception as e:
            # Handle specific rate-limiting (HTTP 429)
            if '429' in str(e):  # Check if it's a rate-limiting error
                print(f"Rate limit exceeded, retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
                delay *= 2  # Exponentially increase the delay
            else:
                print(f"Error during search: {e}")
                return "Error: Unable to fetch results from Google at the moment."
    
    return "Error: Too many retries, please try again later."

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get real-time information like the current date and time.
def Information():
    current_date_time = datetime.datetime.now()
    return (
        f"Use This Real-time Information if needed:\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H:%M:%S')}\n"
    )

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    
    # Load the chat log from the JSON file.
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})
    
    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})
    
    # Generate a response using the Groq client.
    completion = client.chat.completions.create( 
        model = "llama3-70b-8192",
        messages = SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature = .7,
        max_tokens = 2048,
        top_p = 1,
        stream = True,
        stop = None
    )
    
    Answer = ""
    
    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
            
    # Clean up the response.
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    
    # Save the updated chat log back to the JSON file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
        
    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# Main Execution
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
