from googleapiclient.discovery import build
from mail_auto_summrizor.utils.Gmail.credential_utils import get_credential
from mail_auto_summrizor.utils.Gmail import gmail_filter_utils

class GmailSettingHelper:
    def __init__(self, scopes:list):
        '''
        Wrapper for gmail_filter_utils funtions.
        Manages gmail lables, filters and project system cache.
        '''

        # Build gmail service
        creds = get_credential(scopes)
        self.service = build('gmail', 'v1', credentials=creds)

    # ====================================
    # filter wrappers
    # ====================================

    def get_filters(self):
        return gmail_filter_utils.get_filters(self.service)

    def create_filters(self):
        return gmail_filter_utils.create_filters(self.service)

    def delete_filter(self, filter_id):
        return gmail_filter_utils.delete_filter(self.service, filter_id)

    # ====================================
    # label wrappers
    # ====================================

    def update_label_cache(self):
        return gmail_filter_utils.get_labels_from_gmail(self.service)

    def get_label_id(self, label_name):
        return gmail_filter_utils.get_label_by_name(self.service, label_name)

    def create_label(self, label_name):
        return gmail_filter_utils.create_label(self.service, label_name)

    def delete_label(self, label_name):
        return gmail_filter_utils.delete_label(self.service, label_name)

from mail_auto_summrizor.utils.Gmail.gmail_message_utils import (
    get_messages_ids, 
    parse_message,
    get_linkedin_url_from_body
)
from mail_auto_summrizor.utils.paths import CACHE_DIR
import json

def GmailDataHelper(service, max_page_count=15) -> dict[str,dict]:
    '''
    This method integrates all needed process for getting job ids from Gmail.

    Process:
        1. get messages ids from gmail that has JOB_ALERT and not AUTO_SUMMARIZE_COMPLETE
        2. from retrieved messages ids, get message and parse its body to get 'job id':url
        3. save job_id - url mapping into `/caches/jobs_meta.cache.json` and return it

    Return:
        {
            "job_id": { "url" : ${URL} },
            "job_id": { "url" : ${URL} },
        }
    '''

    # [Format]
    # [ {msg_id : thread_id} ]
    unprocessed_job_alert_message_id_list = get_messages_ids(
        service,
        "Label_1",
        q="-label:AUTO_SUMMARIZE_COMPLETE",
        max_page_count=max_page_count
    )

    result = {}

    for job_alert_messeage_id_thread_mapping in unprocessed_job_alert_message_id_list:
        job_id_url_mappings = parse_message(service, job_alert_messeage_id_thread_mapping['id'], get_linkedin_url_from_body)

        result.update(job_id_url_mappings)

    with open(CACHE_DIR/"jobs_meta.cache.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    return result

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.settings.basic',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.modify'
]