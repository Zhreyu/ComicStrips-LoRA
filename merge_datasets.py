import os
import shutil

def count_and_move_unique_jpeg_files(dir1, dir2, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files_seen = set()
    unique_files = set()

    for directory in [dir1, dir2]:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.jpeg') or file.lower().endswith('.jpg'):
                    if file not in files_seen:
                        files_seen.add(file)
                        unique_files.add(os.path.join(root, file))
                    else:
                        if file in unique_files:
                            unique_files.remove(file)

    for file_path in unique_files:
        shutil.copy(file_path, os.path.join(output_dir, os.path.basename(file_path)))

    return len(unique_files)

if __name__ == "__main__":
    dir1 = "CDA"
    dir2 = "dataset_final_unique"
    output_dir = "Dataset"
    total_unique_jpeg_files = count_and_move_unique_jpeg_files(dir1, dir2, output_dir)
    print(f"Total number of unique JPEG files moved: {total_unique_jpeg_files}")