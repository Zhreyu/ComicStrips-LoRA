"""

Script to annotate the images in the Dataset folder using the Local Vison Model through Ollama.

"""


import ollama
from ollama import generate
import glob
import pandas as pd
from PIL import Image

import os
from io import BytesIO

# Load the DataFrame from a CSV file, or create a new one if the file doesn't exist
def load_or_create_dataframe(filename):
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['image_file', 'description'])
    return df

df = load_or_create_dataframe('image_descriptions.csv')

def get_image_files(folder_path):
    # Supported image file extensions
    extensions = ['*.png', '*.jpeg', '*.jpg', '*.gif']
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(f"{folder_path}/{ext}"))
    return image_files

# get the list of image files in the folder you want to process
image_files = get_image_files("Dataset")
image_files.sort()

print(image_files[:3])
print(df.head())

prompt = '''Describe the comicstrip image in a single sentence the main charecter's include (a child Calvin and cat/tiger ). PLEASE JUST OUTPUT THE DESCRIPTION OF THE IMAGE. DO NOT INCLUDE THE PROMPT TEXT IN THE OUTPUT.
for example, if Calvin and Hobbes are fishing, the annotation would be 'Calvin and Hobbes attempt to catch a fish while boating together.'

Example OUTPUT:

Calvin is flying down a hill in his wagon, with Hobbes hanging on tightly behind him.'''

# processing the images 
def process_image(image_file):
    print(f"\nProcessing {image_file}\n")
    # with Image.open(image_file) as img:
    #     with BytesIO() as buffer:
    #         img.save(buffer, format='PNG')
    #         image_bytes = buffer.getvalue()

    full_response = ''
    # Generate a description of the image
    for response in generate(model='llava:13b', 
                             prompt=prompt, 
                             images=[image_file], 
                             stream=True):
        # Print the response to the console and add it to the full response
        print(response['response'], end='', flush=True)
        full_response += response['response']

    # Add a new row to the DataFrame
    df.loc[len(df)] = [image_file, full_response]


for image_file in image_files:
    if image_file not in df['image_file'].values:
        process_image(image_file)

# Save the DataFrame to a CSV file
df.to_csv('image_descriptions.csv', index=False)

