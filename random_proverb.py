import re
import random
import requests
import json
import os

import requests
from bs4 import BeautifulSoup

ESV_API_KEY = os.environ['ESV_API_KEY']
ESV_API_URL = 'https://api.esv.org/v3/passage/text/'

CHAPTER_LENGTHS = [
    33, 22, 35, 27, 23, 35, 27, 36, 18, 32, 31, 28, 25, 35, 33, 33, 28, 24, 29,
    30, 31, 29, 35, 34, 28, 28, 27, 28, 27, 33, 31
]


def get_proverbs():
    chapter = random.randrange(1, len(CHAPTER_LENGTHS))
    verse = random.randint(1, CHAPTER_LENGTHS[chapter])
    text_return = 'Proverbs %s:%s' % (chapter, verse)
    return text_return, chapter, verse


def get_chinese_text(chapter, verse):
    url = f"https://www.biblegateway.com/passage/?search=Proverb {chapter}:{verse}&version=CNVS"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language":
        "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Look for verse container within passage content
    passage_div = soup.find("div", class_="passage-text")
    if not passage_div:
        raise Exception("Could not find passage-text div")

    output = []
    for span in passage_div.find_all("span", class_="text"):
        parent_classes = span.parent.get("class", [])
        # skip if it's a heading, chapternum, or footnote container
        if any(c in ["chapternum", "heading", "footnote", "crossreference"]
               for c in parent_classes):
            continue
        verse_text = span.get_text(strip=True)
        output.append(verse_text)
    return " ".join(output)


def get_esv_text(passage):
    params = {
        'q': passage,
        'indent-poetry': False,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': False
    }

    headers = {'Authorization': 'Token %s' % ESV_API_KEY}

    data = requests.get(ESV_API_URL, params=params, headers=headers).json()

    text = re.sub('\s+', ' ', data['passages'][0]).strip()

    return '%s – %s' % (text, data['canonical'])


def render_esv_text(data):
    text = re.sub('\s+', ' ', data['passages'][0]).strip()

    return '%s – %s' % (text, data['canonical'])
