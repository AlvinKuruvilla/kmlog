import os
import csv
from rich.progress import track
from dotenv import dotenv_values
from supabase import create_client, Client


def sanitize_filename(filename):
    return filename.replace(",", "_")


def replace_js_key(key: str) -> str:
    """
    Replace the JavaScript key with the Python key format.
    """
    if key == "Shift":
        return "Key.shift"
    elif key == "Control":
        return "Key.ctrl"
    elif key == "Alt":
        return "Key.alt"
    elif key == "Meta":
        return "Key.cmd"
    elif key == "Enter":
        return "Key.enter"
    elif key == "Backspace":
        return "Key.backspace"
    elif key == "Escape":
        return "Key.esc"
    elif key == "Tab":
        return "Key.tab"
    elif key == "Space" or key == " ":
        return "Key.space"
    elif key == "ArrowLeft":
        return "Key.left"
    elif key == "ArrowRight":
        return "Key.right"
    elif key == "ArrowUp":
        return "Key.up"
    elif key == "ArrowDown":
        return "Key.down"
    elif key == "CapsLock":
        return "Key.caps_lock"
    else:
        return key


BUCKET_NAME: str = "data-collection-files"
FOLDER_NAME: str = "uploads"
config = dotenv_values(".env")

url: str = config["SUPABASE_URL"]
key: str = config["SUPABASE_KEY"]

supabase: Client = create_client(url, key)
response = supabase.storage.from_(BUCKET_NAME).list(
    FOLDER_NAME,
    {
        "limit": 100,
        "offset": 0,
        "sortBy": {"column": "name", "order": "desc"},
    },
)
all_files = []
for item in response:
    (
        all_files.append(item["name"])
        if item["name"].endswith((".csv", ".txt", ".json"))
        else None
    )
# print(all_files)
unique_user_ids = set()

# Extract unique user IDs from the filenames
for f in all_files:
    unique_user_ids.add(f.split("_")[1])

# Loop through each user ID and download the corresponding files
for user_id in unique_user_ids:
    for f in all_files:
        if user_id in f:
            # Sanitize the filename before writing to disk
            sanitized_filename = sanitize_filename(f)

            # Open the file and write the response to disk with the sanitized filename
            with open(f"./downloads/{sanitized_filename}", "wb+") as download:
                response = supabase.storage.from_(BUCKET_NAME).download(
                    f"{FOLDER_NAME}/{f}"
                )
                download.write(response)
files = os.listdir("downloads")
# Filtering only the files.
files = [f for f in files if os.path.isfile("downloads" + "/" + str(f))]
for f in track(files, description="Processing files..."):
    if f.endswith(".csv"):
        print(f"Processing {f}...")
        try:
            # Open the file and read it manually
            with open(f"./downloads/{f}", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)  # Read all rows into memory

            # Check if the file is empty
            if not rows:
                print(f"Error reading {f}: File is empty.")
                continue

            # Identify the header (assuming the first row is the header)
            header = rows[0]
            key_column_index = header.index("Key")  # Find the column index of 'Key'

            # Process the rows and apply the key replacement function
            for row in rows[1:]:
                row[key_column_index] = replace_js_key(row[key_column_index])

            # Open the file in write mode and overwrite the original file with modified data
            with open(f"./downloads/{f}", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            print(f"Successfully updated {f}")

        except FileNotFoundError:
            print(f"Error reading {f}: File not found.")
            continue
        except csv.Error:
            print(f"Error reading {f}: CSV parsing error.")
            continue
        except UnicodeDecodeError:
            print(f"Error reading {f}: Unicode decode error.")
            continue
