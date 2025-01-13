# to handle general queries
import os
from groq import Groq # Importing the Groq library to use its API.
from json import load, dump # Importing functions to read and write JSON files.
import datetime # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file

# Load environment variables from the .env file.
env_vars = dotenv_values(os.path.join(os.getcwd(), ".env"))

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# define a system message that provides context to AI chatbot about its role and behaviour
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# list of system instructions for chatbot
SystemChatBot = [
    {"role": "system", "content": System}
]

# Define the absolute path to the Data directory
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
chatlog_path = os.path.join(data_dir, 'ChatLog.json')

# attempt to load the chat log from a JSON file
try:
    with open(chatlog_path, "r") as f:
        messages = load(f)  # load existing messages from chat log
except FileNotFoundError:
    # if file doesn't exist, create an empty JSON file to store chat logs
    with open(chatlog_path, "w") as f:
        dump([], f)

# function to get real time date and time info
def RealtimeInformation():
    current_date_time = datetime.datetime.now()  # current date and time
    day = current_date_time.strftime("%A")  # week day
    date = current_date_time.strftime("%d")  # Day of the month.
    month = current_date_time.strftime("%B")  # Full month name.
    year = current_date_time.strftime("%Y")  # Year.
    hour = current_date_time.strftime("%H")  # hour in 24-hour format
    minute = current_date_time.strftime("%M")  # Minute.
    second = current_date_time.strftime("%S")  # Second.

    # Format the information into a string.
    data = (
        f"Please use this real-time information if needed, \n"
        f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
        f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    )
    return data


# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Split the response into lines.
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines)  # Join the cleaned lines back together.
    return modified_answer

# Main chatbot function to handle user queries.
def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response. """
    try:
        # load the existing chat log from the JSON file.
        with open(chatlog_path, "r") as f:
            messages = load(f)

        # append the user's query to the message list
        messages.append({"role": "user", "content": f"{Query}"})

        # make a request to the Groq API for a response
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # AI model
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,  # Include system instructions, real-time info, and chat history.
            max_tokens=1024,  # Limit the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness (higher means more random).
            top_p=1,  # Use nucleus sampling to control diversity.
            stream=True,  # Enable streaming response.
            stop=None  # Allow the model to determine when to stop.
        )

        Answer = ""  # Initialize a string to store AI's response

        # Process the streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # check if there's content in current chunk
                Answer += chunk.choices[0].delta.content  # append content to answer

        Answer = Answer.replace("</s>", "")  # clean up any unwanted tokens from the response

        # Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log to the JSON file.
        with open(chatlog_path, "w") as f:
            dump(messages, f, indent=4)

        # Return the formatted response.
        return AnswerModifier(Answer=Answer)

    except Exception as e:
        # Handle errors by printing the exception and resetting the chat log.
        print(f"Error: {e}")
        with open(chatlog_path, "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)  # Retry the query after resetting the log.


# Main Execution
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question: ")  # prompt user for question
        print(ChatBot(user_input))  # call chatbot function and print the response
