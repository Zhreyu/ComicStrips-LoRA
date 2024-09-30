import os
from PIL import Image

# Directory containing the image files
directory = '/home/ubuntu/finetune-lora/ai-toolkit/output/ComicStrips/ComicStrips_flux_lora_v1_fp16/samples'


# Output folder for GIFs
output_directory = 'GIFS'
os.makedirs(output_directory, exist_ok=True)

# Dictionary to hold file lists categorized by their ending number (0 to 9)
file_groups = {str(i): [] for i in range(10)}

# Function to group images by their ending digit
def group_files_by_ending(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            ending_digit = filename.split('_')[-1].split('.')[0][-1]
            if ending_digit in file_groups:
                file_groups[ending_digit].append(os.path.join(directory, filename))
    return file_groups

# Function to create a GIF from a list of images
def create_gif(image_list, output_file):
    images = [Image.open(img) for img in image_list]
    images[0].save(output_file, save_all=True, append_images=images[1:], loop=0, duration=500)

# Group the files by their ending digit
grouped_files = group_files_by_ending(directory)

# Generate GIFs for each group
for ending_digit, files in grouped_files.items():
    if files:
        output_file = os.path.join(output_directory, f'group_{ending_digit}.gif')
        create_gif(files, output_file)
        print(f'GIF created for group {ending_digit}: {output_file}')
