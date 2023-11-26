# Functions to download podcast episodes from Apple podcast

import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def find_audio_url(html: str) -> str:
    # Find all .mp3 and .m4a URLs in the HTML content
    audio_urls = re.findall(r'https://[^\s^"]+(?:\.mp3|\.m4a)', html)

    # If there's at least one URL, return the first one
    if audio_urls:
        pattern = r'=https?://[^\s^"]+(?:\.mp3|\.m4a)'
        result = re.findall(pattern, audio_urls[-1])
        if result:
          return result[-1][1:]
        else:
          return audio_urls[-1]

    # Otherwise, return None
    return None

def get_file_extension(url: str) -> str:
    # Parse the URL to get the path
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Extract the file extension using os.path.splitext
    _, file_extension = os.path.splitext(path)

    print("url", url, path, file_extension)
    # Return the file extension
    return file_extension

def download_apple_podcast(url: str):
    output_folder = 'Audio'
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f"Error: Unable to fetch the podcast page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    audio_url = find_audio_url(response.text)

    if not audio_url:
        print("Error: Unable to find the podcast audio url.")
        return

    episode_title = soup.find('span', {'class': 'product-header__title'})

    if not episode_title:
        print("Error: Unable to find the podcast title.")
        return

# Remove or replace invalid characters for Windows file names
    episode_title = episode_title.text.strip().replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-')

    # MAC LINE 
    # episode_title = episode_title.text.strip().replace('/', '-')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f"{episode_title}{get_file_extension(audio_url)}")

    with requests.get(audio_url, stream=True) as r:
        r.raise_for_status()
        with open(output_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    if not output_file:
        print("Error: Unable to download podcast.")
    else:
        print(f"Downloaded podcast episode '{episode_title}' to '{output_folder}'")