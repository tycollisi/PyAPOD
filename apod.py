import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from PyWallpaper import change_wallpaper


# Get NASA API Key from .env file in current directory
load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")

# Base URL for NASA endpoints
BASE_URL = 'https://api.nasa.gov'


# Function to get Astronomy Picture Of The Day Data
def get_apod():
    endpoint = f"{BASE_URL}/planetary/apod"
    params = {'api_key': NASA_API_KEY}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        apod_data = response.json()
        return apod_data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to download the image, URL is the link to the image to be downloaded, file_path is the local file path to save the image to.
def download_image(url, file_path):
    # Use the requests library to make a GET request to the URL.
    # 'with' opens the HTTP response with a context manager
    # response is the object returned by the GET request.
    # stream=True allows the response to be streamed, meaning we won't download the whole response content at once.
    with requests.get(url, stream=True) as response:
        # Check for successful status code, otherwise raise exception
        response.raise_for_status()
        # open file in file mode 'wb' which stands for 'write binary'.
        with open(file_path, 'wb') as file:
            # for loop iterates through chunks of data at a time
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

            

# Call the function and print the Astronomy Picture of the Day (APOD) information
apod_data = get_apod()
if apod_data:
    print(f"Title: {apod_data['title']}")
    print(f"Date: {apod_data['date']}")
    print(f"Explanation: {apod_data['explanation']}")
    print(f"Image URL: {apod_data['url']}")

    # Extract the file name from the image URL
    file_name = os.path.basename(apod_data['url'])

    # Specify the directory where you would like to save the image
    # Go to the directory you wish to save to in your terminal, type the command pwd
    save_directory = os.getenv("SAVE_DIRECTORY") 

    # Save the image to the specified directory
    file_path = os.path.join(save_directory, file_name)
    download_image(apod_data['url'], file_path)
    print(f"Image saved to: {file_path}")

    # Load the jpg image
    image = Image.open(file_path)

    # Create a transparent image
    transparent_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # Create a drawing object
    draw = ImageDraw.Draw(transparent_image)
    
    # Extract the full explanation from the APOD data
    full_explanation = apod_data['explanation']

    # Define the maximum words per line
    max_words_per_line = 6
    
    # Split the full explanation into words
    words = full_explanation.split()

    # Split the words into lines based on the maximum number of words
    text_lines = [' '.join(words[i:i + max_words_per_line]) for i in range(0, len(words), max_words_per_line)]

    # Combine the lines into a single string with line breaks
    limited_explanation_text = "\n".join(text_lines)
    
    # Specify the text and add position
    text = f"Title: {apod_data['title']}\nAPOD: {apod_data['date']}\nExplanation:\n{limited_explanation_text}"

    # Choose a font and font size
    font = ImageFont.truetype("/Users/tycollisi/Dropbox/python-folders/APOD/font/AstroSpace.ttf", size=18)  # Change the font path and size as needed

    # Set the text position using x, y variables
    x = 0
    y = 10

    # Choose RGB text color, 128 = 50% transparent
    text_color = (255, 255, 255, 70)  # RGB values for white color, change as needed

    # Add the text to the image
    draw.text((x, y), text, fill=text_color, font=font) 

    # Overlay the transparent image with text onto the original image
    final_image = Image.alpha_composite(image.convert("RGBA"), transparent_image)

    # Specify the directory where you would like to save the updated image
    # Go to the directory you wish to save to in your terminal, type the command pwd
    updated_save_directory = os.getenv("UPDATED_SAVE_DIRECTORY")
    
    # Save the modified image
    final_image_file_name = f"updated_{file_name}.png"
    final_image.save(os.path.join(updated_save_directory, final_image_file_name))
    

    # Store the path where the final image will be saved
    final_image_path = f"{updated_save_directory}/{final_image_file_name}"

    print(f"Final image saved to: {final_image_path}")
    change_wallpaper(final_image_path)

    
    