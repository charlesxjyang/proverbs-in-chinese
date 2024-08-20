import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googletrans import Translator
import random
import pypinyin
from random_proverb import get_esv_text, get_proverbs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ESV_API_KEY = os.getenv('ESV_API_KEY')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

def get_random_proverb():
    return get_esv_text(get_proverbs())

def translate_to_chinese(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='zh-cn')
    return translation.text

def get_pinyin(chinese_text):
    pinyin_list = pypinyin.lazy_pinyin(chinese_text)
    return ' '.join(pinyin_list)

def send_email(proverb, chinese_translation, pinyin, sender_email, receiver_email, password):
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
    proverb = get_random_proverb()
    chinese_translation = translate_to_chinese(proverb)
    pinyin = get_pinyin(chinese_translation)

    # Use environment variables for email credentials
    sender_email = os.getenv('EMAIL_SENDER')
    receiver_email = os.getenv('EMAIL_RECEIVER')
    password = os.getenv('EMAIL_PASSWORD')

    send_email(proverb, chinese_translation, pinyin, sender_email, receiver_email, password)

if __name__ == "__main__":
    main()
