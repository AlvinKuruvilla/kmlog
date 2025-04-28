from dotenv import dotenv_values
from supabase import create_client, Client

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
    all_files.append(item["name"]) if item["name"].endswith(
        (".csv", ".txt", ".json")
    ) else None
# print(all_files)
unique_user_ids = set()
for f in all_files:
    unique_user_ids.add(f.split("_")[1])
print(unique_user_ids)

for user_id in unique_user_ids:
    for f in all_files:
        if user_id in f:
            with open(f"./downloads/{f}", "wb+") as download:
                response = supabase.storage.from_(BUCKET_NAME).download(
                    f"{FOLDER_NAME}/{f}"
                )
                download.write(response)
