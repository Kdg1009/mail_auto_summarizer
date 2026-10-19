import json
from time import sleep

import requests
from googleapiclient.discovery import build
from mail_auto_summrizor.utils.paths import CACHE_DIR
from mail_auto_summrizor.utils.LinkedIn.data_mining_utils import LinkedInDataHelper
from mail_auto_summrizor.utils.Gmail.credential_utils import get_credential
from mail_auto_summrizor.utils.Gmail.gmail_message_utils import GmailDataHelper
from mail_auto_summrizor.utils.Gmail.gmail_filter_utils import create_label

def save_cache(cache, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(cache, file, ensure_ascii=False, indent=4)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.settings.basic',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.modify'
]

def main():
    creds = get_credential(SCOPES)
    service = build('gmail','v1',credentials=creds)

    gmail_output = GmailDataHelper(service,1)
    LinkedInDataHelper(gmail_output)

if __name__ == "__main__":
    main()