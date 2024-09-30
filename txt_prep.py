"""Script to create text files for each image in the Dataset folder with the corresponding description from a CSV file. This is done in order to prepare the dataset for finetuning Flux."""

import os
import csv

dataset_folder = 'Dataset'  # Path where your images are stored
csv_file = 'image_descriptions.csv'  # Path to your CSV file

# Create the text files for each image in the dataset folder
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    
    # Skip the header row
    next(reader)
    
    for row in reader:
        image_file, description = row
        
        # Extract the base name (without extension) for the image file
        image_name = os.path.splitext(os.path.basename(image_file))[0]
        
        # Create the corresponding text file with the description
        txt_file_path = os.path.join(dataset_folder, f"{image_name}.txt")
        
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(description)

print("Text files created successfully.")
