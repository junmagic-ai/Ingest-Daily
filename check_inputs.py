import re

def identify_url_type(url):
    youtube_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'
    apple_pattern = r'(https?://)?(www\.)?podcasts\.apple\.com/.+/podcast/.+'

    if re.match(youtube_pattern, url):
        return 'YouTube'
    elif re.match(apple_pattern, url):
        return 'Apple'
    else:
        return 'Unknown'
