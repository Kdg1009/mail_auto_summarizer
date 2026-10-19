import json
from time import sleep
from random import randint
import requests

from mail_auto_summrizor.utils.cache.cache_utils import save_cache
from mail_auto_summrizor.utils.LinkedIn.data_mining_utils import get_job_data_from_url
from mail_auto_summrizor.utils.paths import CACHE_DIR

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

            # Save after each data extraction because this prevents 429 client error.
            save_cache(job_data_cache, info_path)

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

        #sleep(randint(1,10))