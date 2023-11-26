import os
from  get_sources import fetch_and_complete_tasks
from check_inputs import identify_url_type
from get_pod import download_apple_podcast
from get_tube import YouTubeDownloader
from transcribe import transcribe_audio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from summariser import summarise
import os
from notion import update_notion

if __name__ == '__main__':
    folders = ['Audio', 'Texts', 'Processed', 'Summaries']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    sources = fetch_and_complete_tasks()
    for item in sources:
        if(identify_url_type(item['title']) != 'Unknown'): 
            item_type =identify_url_type(item['title'])
            if (item_type == 'YouTube'):
                downloader = YouTubeDownloader(item['title']).execute()
            elif (item_type == 'Apple'):
                download_apple_podcast(item['title'])

    transcribe_audio()

    for file in os.listdir('Audio'):
        if os.path.isfile(f'Audio/{file}'): 
            os.remove(f'Audio/{file}')

    text_files = os.listdir('Texts')
    for file in text_files:
        if os.path.isfile(f'Texts/{file}'):  # Add this line
            with open(f'Texts/{file}', 'r') as f:
                content = f.read()

            final_summary = ''
            if len(content) > 5000:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
                chunks = text_splitter.split_text(content)
                for chunk in chunks:
                    summary = summarise(chunk)
                    final_summary += summary + '\n'
            else:
                final_summary = summarise(content)

            with open(f'Summaries/{file}', 'w') as f:
                f.write(final_summary)
        if os.path.isfile(f'Texts/{file}'):
            os.rename(f'Texts/{file}', f'Texts/Processed/{file}')

    update_notion()

    summ_files = os.listdir("Summaries")
    for file in summ_files:
        if os.path.isfile(f'Summaries/{file}'):
            os.rename(f'Summaries/{file}', f'Summaries/Processed/{file}')