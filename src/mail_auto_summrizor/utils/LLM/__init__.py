import json
import time

from mail_auto_summrizor.utils.paths import CACHE_DIR

from mail_auto_summrizor.utils.LLM.utils.sumary_utils import summary_job_data, warmup_model

def LLMDataHelper(model:str, verbose:bool = True, enable_time_log:bool = False):
    '''
    This helper reads caches/jobs_info.cache.json and summary its content into structured json format.
    and write json file into caches/jobs_summary.cache.json
    [Output format]
    {
        company: str
        job_title: str
        responsibilities: list
        experience_requirements: list
        required_skills: list
        preferred_skills: list
        soft_skills: list
        employment_type: list
    }
    '''
    start = time.perf_counter()
    #warmup_model(model)

    with open(CACHE_DIR/"jobs_info.cache_.json", 'r', encoding='utf-8') as f:
        jobs_infos = json.load(f)

    results = {}

    for job_id, job_info in jobs_infos.items():
        if verbose:
            print(f'[INFO] Processing {job_info['company']}({job_id})')

        result = summary_job_data(job_info, verbose, enable_time_log)
        results[job_id] = result

    with open(CACHE_DIR/"jobs_summary.cache.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    elapsed = time.perf_counter() - start
    print(f'[INFO] Total time: {elapsed:.2f}s')