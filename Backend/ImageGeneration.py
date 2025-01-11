# images will be generated according to the given description

import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
from time import sleep
import os

#Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data" #Folder where the images are stored
    prompt = prompt.replace(" ", "_") # Replace spaces in prompt with underscores

    # Generate the filenames for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path= os.path.join(folder_path, jpg_file)

        try:
            #Try to open and display the image 
            img = Image.open(image_path)
            print(f"Opening image: {image_path}") 
            img.show()
            sleep(1) # Pause for 1 second before showing the next image

        except IOError:
            print(f"Unable to open {image_path}")

#API details for the Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0" 
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

#Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload) 
    return response.content

#Async function to generate images based on the given prompt
async def generate_images (prompt: str):
    tasks = []

    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    #Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)

    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i+1}.jpg", "wb") as f:
            f.write(image_bytes)

# wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt)) # run the async image generation
    open_images(prompt) # open generated images

        
# Main execution loop
while True:
    try:
        # Check if the ImageGeneration.data file exists
        data_file = "Frontend/Files/ImageGeneration.data"
        if not os.path.exists(data_file):
            with open(data_file, "w") as f:
                f.write("False,False")

        # Read prompt and status from file
        with open(data_file, "r") as f:
            data = f.read()

        prompt, status = data.split(",")

        if status.strip() == "True":
            print("Generating Images...")
            GenerateImages(prompt.strip())

            # Reset the status after generating images
            with open(data_file, "w") as f:
                f.write("False,False")

            break  # Exit after processing the request
        else:
            sleep(1)  # Wait before re-checking the file

    except Exception as e:
        print(f"Error: {e}")
        sleep(1)  # Retry after a short delay