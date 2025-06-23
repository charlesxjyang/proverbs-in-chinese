import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pypinyin import pinyin, Style
from random_proverb import get_esv_text, get_proverbs, get_chinese_text
import os

import json

#with open('config.json') as config_file:
#   config = json.load(config_file)

import os
import json

ESV_API_KEY = os.environ['ESV_API_KEY']
EMAIL_SENDER = os.environ['EMAIL_SENDER']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_RECEIVER = json.loads(os.environ['EMAIL_RECEIVER'])
# Replace 'your-api-key' with you\


def get_random_proverb():
    proverbs_data, chapter, verse = get_proverbs()
    return get_esv_text(proverbs_data), get_chinese_text(chapter, verse)


def get_pinyin(chinese_text):
    # Get pinyin with tones
    pinyin_with_tones = pinyin(chinese_text, style=Style.TONE3)

    # Flatten the list of lists into a single string
    pinyin_with_tones_flat = ' '.join([item[0] for item in pinyin_with_tones])

    return pinyin_with_tones_flat


def send_email(proverb, chinese_translation, pinyin, sender_email,
               receiver_email, password):
    subject = "Daily Proverb"

    # Create the email content
    body = f"""
    Proverb: {proverb}

    Simplified Chinese: {chinese_translation}

    Pinyin: {pinyin}
    """

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def main():
    proverb, chinese_proverb = get_random_proverb()
    pinyin = get_pinyin(chinese_translation)
    for receiver in EMAIL_RECEIVER:
        send_email(proverb, chinese_translation, pinyin, EMAIL_SENDER,
                   receiver, EMAIL_PASSWORD)


if __name__ == "__main__":
    main()
