import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os

def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        image.save(save_path)
        print(f"Image downloaded from {url} and saved to {save_path}")
    except requests.exceptions.MissingSchema:
        print(f"Invalid URL format in CSV: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def download_images_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        for index, row in df.iterrows():
            image_name = row["isbn"]
            url = row["url"]
            save_path = f"images/{image_name}.jpg"  # เปลี่ยนตามต้องการ
            os.makedirs("images", exist_ok=True)
            download_image(url, save_path)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
csv_file = "book.csv"  # Replace with your CSV file path
download_images_from_csv(csv_file)
