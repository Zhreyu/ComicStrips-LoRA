import os
from PIL import Image

# Supported image file extensions
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')

def resize_images_in_folder(folder_path, size=(512, 512)):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    # Get a list of all files in the folder
    for filename in os.listdir(folder_path):
        # Create the full path to the image file
        file_path = os.path.join(folder_path, filename)

        # Skip non-image files based on their extension
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            print(f"Skipping non-image file: {filename}")
            continue

        try:
            # Open the image file
            with Image.open(file_path) as img:
                # Resize the image
                img_resized = img.resize(size)
                # Save the image with the same name, replacing the original
                img_resized.save(file_path)
                print(f"Resized and saved: {filename}")

        except Exception as e:
            print(f"Error processing file '{filename}': {e}")

if __name__ == "__main__":
    folder_path = "Dataset"
    resize_images_in_folder(folder_path)
