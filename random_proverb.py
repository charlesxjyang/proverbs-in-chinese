import re
import random
import requests

ESV_API_KEY = os.environ['ESV_API_KEY']
BIBLE_API_KEY = os.environ['BIBLE_API_KEY']
BIBLE_API_URL = 'https://api.scripture.api.bible/v1/bibles/'
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
    url = f"{BIBLE_API_URL}/books/13/"
    headers = {"api-key": BIBLE_API_KEY}
    response = requests.get(BIBLE_API_URL, headers=headers)
    print(response)
    if response.status_code == 200:
        data = response.json()
        verse_text = data.get('data', {}).get('content', '').strip()
        return verse_text
    else:
        raise Exception(
            f"Failed to fetch verse: {response.status_code} - {response.text}")


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
