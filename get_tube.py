import yt_dlp
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeDownloader:
    def __init__(self, video_url):
        self.video_url = video_url
        self.output_dir = 'Audio'
        self.texts_dir = 'Texts'
        self.video_id = self._extract_video_id()

    def _extract_video_id(self):
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', self.video_url)
        return match.group(1) if match else None

    def download_audio(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}], 'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s')}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_url])

    def download_transcript(self):
        if not self.video_id:
            print("Invalid video URL.")
            return False

        if not os.path.exists(self.texts_dir):
            os.makedirs(self.texts_dir)

        try:
            transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages=['en'])
            video_title = self._sanitize_title_for_filename()
            transcript_path = os.path.join(self.texts_dir, f'{video_title}.txt')
            self._save_transcript(transcript, transcript_path)
            return True
        except Exception as e:
            print(f"Error downloading transcript: {e}")
            return False

    def _sanitize_title_for_filename(self):
        ydl_opts = {'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.video_url, download=False)
            return "".join(c if c.isalnum() or c in (' ', '.', '-', '_') else '' for c in info['title']).rstrip()

    def _save_transcript(self, transcript, path):
        with open(path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(entry['text'] + ' ')

    def execute(self):
        if not self.download_transcript():
            self.download_audio()

# Example usage


