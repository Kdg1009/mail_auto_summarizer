from mail_auto_summrizor.utils.paths import CACHE_DIR
from mail_auto_summrizor.utils.LLM.data_interface_manage import payloads
from mail_auto_summrizor.utils.LLM.data_interface_manage import schemas
from mail_auto_summrizor.tags.utils.search_utils import TagEmbeddingSearch
from mail_auto_summrizor.utils.LLM.utils.response_styles import request_LLM_to_make_tag

MODEL = "gemma2:9b-instruct-q8_0"

JOB_INFO_CACHE = CACHE_DIR / "jobs_info.cache.json"

def summary_job_data(job_data: dict, tag_searcher: TagEmbeddingSearch, verbose:bool = True, enable_time_log:bool = True):
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
    time_logs = []

    # 1. Extract company, job title
    company = job_data.get("company")
    job_title = job_data["job_title"]
    description = job_data["description"]
    content['company'] = company

    response, time_log = request_LLM_to_make_tag(
        MODEL,
        job_title,
        payloads.JOB_TITLE_EVIDENCE_EXTRACTION_RULE_SCRIPT,
        payloads.JOB_TITLE_TAG_SCRIPT,
        schemas.JOB_TITLE_SCHEMA,
        tag_searcher,
        ["industrial_domain","job_family","seniority"],
        verbose
    )
    content.update(response)
    time_logs.append(time_log)

    # 2. Extract responsibilities
    response, time_log = request_LLM_to_make_tag(
        MODEL,
        description,
        payloads.RESPONSIBILITIES_EVIDENCE_EXTRACTION_RULE_SCRIPT,
        payloads.RESPONSIBILITIES_TAG_SCRIPT,
        schemas.RESPONSIBILITIES_SCHEMA,
        tag_searcher,
        ["task_area"],
        verbose
    )
    content.update(response)
    time_logs.append(time_log)
    
    # 3. Extract required skills, preferred skills and experiences 
    response, time_log = request_LLM_to_make_tag(
        MODEL,
        description,
        payloads.SKILLS_EVIDENCE_EXTRACTION_RULE_SCRIPT,
        payloads.SKILLS_TAG_SCRIPT,
        schemas.SKILLS_SCHEMA,
        tag_searcher,
        ["skill","industrial_domain","experience_type"],
        verbose
    )
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