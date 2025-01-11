# here will be the answer of jarvis convert his answer to a voice mail


import pygame # for handling audio playback 
import random #for generating random choices
import asyncio # for asynchronous operations
import edge_tts # for text-to-speech functionality
import os # for file path handling
from dotenv import dotenv_values # for reading environment variables from a .env file

# load environment variables from .env file
env_vars = dotenv_values(os.path.join(os.getcwd(), ".env"))
AssistantVoice = env_vars.get("AssistantVoice") # Get the AssistantVoice from the environment variables


#Asynchronous function to convert text to an audio file 
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3" #Define the path where the speech file will be saved
    
    if os.path.exists(file_path): # Check if the file already exists
        os.remove(file_path) # If it exists, remove it to avoid overwriting errors
        
    # Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%') 
    await communicate.save(r'Data\speech.mp3') #Save the generated speech as an MP3 file
    
#Function to manage Text-to-Speech (TTS) functionality 
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously 
            asyncio.run(TextToAudioFile(Text))
            #Initialize pygame mixer for audio playback 
            pygame.mixer.init()
            #Load the generated speech file into pygame mixer 
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play() # Play the audio
            
            #Loop until the audio is done playing or the function stops 
            while pygame.mixer.music.get_busy():
                if func() == False: #Check if the external function returns False
                    break
                pygame.time.wait(100) #Limit the loop to 10 ticks per second
            
            return True # Return True if the audio played successfully
        except Exception as e: # Handle any exceptions during the process 
            print(f"Error in TTS: {e}")

        finally: 
            try:
                #Call the provided function with False to signal the end of TTs
                func(False)
                pygame.mixer.music.stop() # stoop audio playback
                if pygame.mixer.get_init():
                    pygame.mixer.quit()

            
            except Exception as e: # handle exceptions during cleanup
                print(f"Error in finally block: {e}")
                
#Function to manage Text-to-Speech with additional responses for long text
def TextToSpeech (Text, func=lambda r=None: True):
    Data = [sentence.strip() for sentence in str(Text).split(".") if sentence.strip()] #Split the text by periods into a list of sentences
    
    #List of predefined responses for cases where the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    
    # If the text is very long (more than 4 sentences and 250 characters), add a response message 
    if len(Data) > 4 and len(Text) >= 250:
        summary = ". ".join(Data[:2]) + "."
        TTS(summary + " " + random.choice(responses), func)

    
    # otherwise, just play the whole text
    else:
        TTS(Text, func)
    

# main execution
if __name__ == "__main__":
    while True:
        # Get user input
        TextToSpeech(input("Enter the text: "))
        