import os
import yaml
import csv
from pathlib import Path

if __name__ == "__main__":
    dir_name = "users/"
    user_files = os.listdir()
    dir_path = os.path.join(os.getcwd(), dir_name)
    header = ["ID", "Gender"]
    data = []
    id_cache = []
    with open("Demographics.csv", "w", encoding="utf8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        selected_profile_path = os.path.join(dir_path)
        user_files = os.listdir(selected_profile_path)
        for profile in user_files:
            file_path = selected_profile_path = os.path.join(dir_path, profile)
            with open(file_path, "r") as f:
                user_data = yaml.load(f, Loader=yaml.FullLoader)
                print(user_data)
                user_id = Path(file_path).stem
                gender = user_data["gender"]
                if not user_id in id_cache:
                    data.append(user_id)
                    data.append(gender)
                    writer.writerow(data)
                    id_cache.append(user_id)
                data = []
