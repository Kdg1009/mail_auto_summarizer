import json
from mail_auto_summrizor.utils.paths import CACHE_DIR, TEST_DIR
from mail_auto_summrizor.utils.LLM.utils.response_styles import record_response_time_cost
from mail_auto_summrizor.utils.LLM.data_interface_manage import payloads
from mail_auto_summrizor.utils.LLM.data_interface_manage import schemas
from mail_auto_summrizor.utils.LLM.utils.preprocess_utils import PREPROCESS_PIPELINE

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma2:9b-instruct-q8_0"

JOB_INFO_CACHE = CACHE_DIR / "jobs_info.cache.json"

def summary_job_data(job_data: dict, verbose:bool = True, enable_time_log:bool = True):
    '''
    Analyze a job posting using local Ollama and return a dict.
    
    [job_data format]
    {
        "page_title":str,
        "job_title":str,
        "company":str,
        "work_mode":str,
        "employment_type":str,
        "description":str,
        "received_at":str
    }

    Returns:
    - content

    [content format]
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

    content = {}
    schema = None
    sys_prompt = None

    time_logs = []

    # 1. Extract company, job title
    company = job_data.get("company")
    job_title = job_data["job_title"]
    description = job_data["description"]

    # Preprocess description
    for fn in PREPROCESS_PIPELINE:
        description = fn(description, company=company)

    content['company'] = company

    schema = schemas.JOB_TITLE_SCHEMA
    sys_prompt = payloads.JOB_TITLE_SYS_CONTENT

    payload = payloads.create_payload(job_title, MODEL, schema, sys_prompt)
    response, time_log = record_response_time_cost(OLLAMA_URL, payload, verbose)
    content.update(response)
    time_logs.append(time_log)

    # 2. Extract responsibilities
    schema = schemas.RESPONSIBILITIES_SCHEMA
    sys_prompt = payloads.RESPONSIBILITIES_SYS_CONTENT

    payload = payloads.create_payload(description, MODEL, schema, sys_prompt)
    response, time_log = record_response_time_cost(OLLAMA_URL, payload, verbose)
    content.update(response)
    time_logs.append(time_log)
    
    # 3. Extract required skills, preferred skills and experiences 
    schema = schemas.SKILLS_SCHEMA
    sys_prompt = payloads.SKILLS_SYS_CONTENT

    payload = payloads.create_payload(description, MODEL, schema, sys_prompt)
    response, time_log = record_response_time_cost(OLLAMA_URL, payload, verbose)
    content.update(response)
    time_logs.append(time_log)

    if enable_time_log:
        content.update({
            "time_log":time_logs
        })

    return content

import requests
def warmup_model(model) -> None:
    '''
    Pre-load model to prevent load model for every request.
    Call this function in starting app.
    
    keeps model alive for 10min.
    '''
    requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "keep_alive": "10m",
        },
        timeout=180,
    ).raise_for_status()

if __name__ == "__main__":
    with open(JOB_INFO_CACHE, "r", encoding="utf-8") as f:
        job_data = json.load(f)

    job = job_data.get("4457489696")
    description = job["description"]
    length = len(description)

    #job["description"] = description[:length//2]

    warmup_model(MODEL)
    result = summary_job_data(job)

    with open(TEST_DIR / f"{MODEL.split(":")[0]}.3.1.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)