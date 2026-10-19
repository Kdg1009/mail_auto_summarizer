def apply_label_to_messages(service, label_id:str, query, iter_page_num=3):
    """
    This function will be deprecated.
    I wrote this function because 'JOB ALERT' label is not applied for previous mails.
    This function actually give influence to Gmail, so you must use this carefully.
    """

    user_input = input(
        "This function must be executed only once and cannot be undone.\n"
        "Do you want to execute? [Y/N]: "
    )

    if user_input != 'Y':
        print("[INFO] Job cancelled")
        return

    message_ids = []
    page_token = None
    page_cnt = 0

    while True:
        result = (
            service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    pageToken=page_token,
                )
                .execute()
        )

        message_ids.extend(msg["id"] for msg in result.get("messages",[]))

        page_token = result.get("nextPageToken")
        page_cnt += 1

        if not page_token or page_cnt >= iter_page_num:
            break

    if not message_ids:
        print(f"[WARNING] No messages found in given query: {query}")
        return

    # There is a limit of 1000 ids per request.
    for i in range(0,len(message_ids),1000):
        (
            service.users()
                .messages()
                .batchModify(
                    userId="me",
                    body={
                        "ids": message_ids[i:i+1000],
                        "addLabelIds": [label_id]
                    }
                )
                .execute()
        )

def get_messages_ids(
        service,
        labelIds:str | None=None, 
        q:str | None=None,
        max_page_count:int=1,
        maxResult=None
    ) -> list[dict[str,str]]:
    """
    This method returns [ { 'id':$ID, 'threadId':$THREADID } ]
    """

    nextToken = None
    page_cnt = 0

    result_messages = []

    while True:
        result = service.users().messages().list(
            userId="me",
            labelIds=labelIds,
            q=q,
            pageToken=nextToken,
            maxResults=maxResult
        ).execute()

        # Each message resource contains only an id and thread id.
        # Additional message details can be fetched using the messages.get method.
        messages = result.get("messages", [])
        result_messages.extend(messages)

        next_token = result.get("nextPageToken")
        page_cnt += 1

        if not next_token or page_cnt >= max_page_count:
            break

    return result_messages

from typing import Callable
def parse_message(service, message_id:str, parse_func:Callable) -> dict[str, dict]:
    """
    Get message from Gmail and parse its body.
    Execute nessary works.
    """

    result = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = result.get("payload")

    return parse_func(payload)

# ===============================================
# Methods for extracting information from message
# ===============================================

import base64

def get_linkedin_url_from_body(payload, jobs=None) -> dict[str,dict]:
    """
    Output format:
        {
            'job id 0' : { 'url' : $URL },
            'job id 1' : { 'url' : $URL }, ...
        }
    """
    
    if jobs is None:
        jobs = {}

    mimeType = payload.get("mimeType", "")

    # If mimeType is 'multipart/alternative', then recursively decode and fetch url from parts.
    if mimeType.startswith("multipart/"):
        for part in payload.get("parts",[]):
            get_linkedin_url_from_body(part, jobs)

    # Get urls from 'text/html'
    # Payload's data is base64url encoded string.
    elif mimeType == "text/html":
        data = payload.get("body",{}).get("data")

        if not data:
            return jobs
        
        html_data = base64.urlsafe_b64decode(data).decode("utf-8")

        jobs.update(extract_jobs(html_data))

    return jobs

from bs4 import BeautifulSoup
import re

def extract_jobs(html:str):
    soup = BeautifulSoup(html, "html.parser")

    jobs = {}

    for a in soup.select('a[href*="linkedin.com"]'):
        url = a["href"]

        # Get job ID
        match = re.search(r"/jobs/view/(\d+)", url)
        if not match:
            continue

        job_id = match.group(1)

        jobs[job_id] = {
            "url": url
        }

    return jobs