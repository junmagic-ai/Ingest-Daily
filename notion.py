import os
import requests
from dotenv import load_dotenv

def read_files_from_folder(folder_path):
    files_content = {}
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), 'r') as f:
                files_content[file] = f.read()
    return files_content

def format_for_notion(file_name, file_content):
    max_length = 2000
    # Splitting the file content into chunks of 2000 characters each
    paragraphs = [file_content[i:i+max_length] for i in range(0, len(file_content), max_length)]

    # Creating a list of paragraph blocks with properly defined rich_text fields
    children_blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": paragraph}}]
            }
        } for paragraph in paragraphs
    ]

    return {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [{"type": "text", "text": {"content": file_name}}],
            "children": children_blocks
        }
    }
def upload_to_notion(formatted_content, notion_token, page_id):
    
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {"children": [formatted_content]}
    response = requests.patch(url, json=data, headers=headers)
    # Debugging: Print out the full error response from Notion
    if response.status_code != 200:
        print(f"Error response content: {response.text}")  # This will show the detailed error message
    
    return response



'''

Where can I find my page's ID?

Open the page in Notion. Use the Share menu to Copy link. Now paste the link in your text editor so you can take a closer look. The URL ends in a page ID.
It should be a 32 character long string. Format this value by inserting hyphens (-) in the following pattern: 8-4-4-4-12 (each number is the length of characters between the hyphens).
Example: 1429989fe8ac4effbc8f57f56486db54 becomes 1429989f-e8ac-4eff-bc8f-57f56486db54.
This value is your page ID.

See here to build Integration: https://developers.notion.com/docs/create-a-notion-integration 

Integration permissions
Before an integration can interact with your Notion workspace page(s), the page must be manually shared with the integration. To share a page with an integration, visit the page in your Notion workspace, click the ••• menu at the top right of a page, scroll down to Add connections, and use the search bar to find and select the integration from the dropdown list.

'''
def update_notion():
    load_dotenv()

    notion_token= os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_PAGEID")
    folder_path = "Summaries"
    notion_token = "secret_UB542CYPbhfmrBvqzNvHemCvuZBngp7YNZ4fjp0y6nC"

    files_content = read_files_from_folder(folder_path)
    for file_name, content in files_content.items():
        formatted_content = format_for_notion(file_name, content)
        response = upload_to_notion(formatted_content, notion_token, page_id)
        if response.status_code == 200:
            print(f"Successfully uploaded {file_name} to Notion.")
        else:
            print(f"Failed to upload {file_name}. Status code: {response.status_code}")

    