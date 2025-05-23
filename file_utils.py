import os
import datetime

def create_timestamp_folder():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join("runs", timestamp)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_text(folder_path, filename, text):
    with open(os.path.join(folder_path, filename), "w") as f:
        f.write(text)

def save_image(folder_path, filename, image_data):
    with open(os.path.join(folder_path, filename), "wb") as f:
        f.write(image_data)
