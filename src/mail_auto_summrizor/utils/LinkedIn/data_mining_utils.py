import requests
from bs4 import BeautifulSoup
import browser_cookie3

from mail_auto_summrizor.utils.paths import CACHE_DIR
from mail_auto_summrizor.utils.cache.cache_utils import save_cache
import json
from time import sleep
from random import randint

def LinkedInDataHelper(gmail_response:dict[str,dict], keep_log=False):
    '''
    This method will handle output result of parse_message().
    
    Need caching system because of LinkedIn response system.
    It returns `requests.exceptions.HTTPError:
                    429 Client Error: Too Many Requests.` if it thinks requests is made by crawler. 
    
    [NOTICE]

    keep_log parameter must be synchronize with => 아마 jobs_meta.cache도 job id 한번 가져오고 캐싱하는게 편할 듯(이거랑 싱크 맞추는 걸 지금 생각 중)
    '''
    meta_path = CACHE_DIR / "jobs_meta.cache.json"
    info_path = CACHE_DIR / "jobs_info.cache.json"

    with open(meta_path, 'r', encoding='utf-8') as file:
        job_id_url_mappings = json.load(file)

    if keep_log and info_path.exists():
        with open(info_path, 'r', encoding='utf-8') as file:
            job_data_cache = json.load(file)
    else:
        job_data_cache = {}

    for job_id in job_id_url_mappings:

        # Skip cached job alert.
        if job_id in job_data_cache.keys():
            continue

        url = f"https://www.linkedin.com/jobs/view/{job_id}"

        try:
            job_data = get_job_data_from_url(url)

            if not job_data:
                print(f'[WARNING] {job_id}: Data is empty.')
                continue

            job_data_cache[job_id] = job_data
            print(f'[INFO] Get {job_id} info successfully.')

        except requests.exceptions.HTTPError as e:
            status_code = (
                e.response.status_code
                if e.response is not None
                else None
            )

            print(f'[ERROR] HTTP error ({job_id}): {e}')

            save_cache(job_data_cache, info_path)
            break

        except requests.exceptions.RequestException as e:
            print(f'[ERROR] Request error ({job_id}): {e}')

        sleep(randint(1,10))

def get_job_data_from_url(url:str):
    cookies = browser_cookie3.chromium(
        domain_name=".linkedin.com"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
            timeout=15
        )
        response.encoding = "utf-8"
        response.raise_for_status()
        
    except requests.exceptions.ConnectionError as e:
        print(f'[ERROR] Network connetion error: {e}')
    
    except requests.exceptions.Timeout:
        print(f'[WARNING] Connection Timeout')

    html = response.text

    return parse_job_html(html)

# ========================================
# get_job_data_from_url 내부에서 사용되는 함수
# ========================================

def parse_job_html(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # 페이지 제목
    page_title = (
        soup.title.get_text(strip=True)
        if soup.title else None
    )

    # 검색창에 표시되는 공고 제목
    title_element = soup.select_one(
        ".search-bar__full-placeholder"
    )
    job_title = (
        title_element.get_text(" ", strip=True)
        if title_element else None
    )

    # 회사 이름
    company_element = soup.select("a.topcard__org-name-link")
    company = company_element[0].text.strip() if company_element else None

    # 공고 상세 설명
    description_element = soup.select_one(
        ".description__text"
    )
    description = (
        description_element.get_text("\n", strip=True)
        if description_element else None
    )

    return {
        "page_title": page_title,
        "job_title": job_title,
        "company": company,
        "description": description,
    }