import json
import time

from mail_auto_summrizor.utils.paths import CACHE_DIR
from mail_auto_summrizor.utils.LLM.utils.sumary_utils import summary_job_data, warmup_model
from mail_auto_summrizor.tags.utils.search_utils import TagEmbeddingSearch

def LLMDataHelper(model:str, tag_searcher: TagEmbeddingSearch, verbose:bool = True, enable_time_log:bool = False, flush_interval: int=20):
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
        employment_type: list
    }
    '''
    assert flush_interval > 0

    # Warm up model
    start = time.perf_counter()
    warmup_model(model)

    input_path = CACHE_DIR/"jobs_info.cache.json"
    output_path = CACHE_DIR/"jobs_summary.cache.json"

    # Load jobs info json file
    with open(input_path, 'r', encoding='utf-8') as f:
        jobs_infos = json.load(f)

    # Initialize results
    if output_path.exists():
        with open(output_path,'r',encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = {}
    processed = len(results)

    def flush():
        temp_path = output_path.with_suffix('.tmp')

        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        temp_path.replace(output_path)

    total = len(jobs_infos)
    for i, (job_id, job_info) in enumerate(jobs_infos.items()):
        if processed > i:
            continue
        if verbose:
            print(f'[INFO] [{i}/{total}] Processing {job_info['company']}({job_id})')

        result = summary_job_data(job_info, tag_searcher, verbose, enable_time_log)
        results[job_id] = result

        if (i+1) % flush_interval == 0:
            flush()

    flush()

    elapsed = time.perf_counter() - start
    print(f'[INFO] Total time: {elapsed:.2f}s')

if __name__ == "__main__":
    # Test code for tag search and tagging performance
    
    from pathlib import Path
    taxonomy_root_path = Path(__file__).parent.parent.parent / 'tags' / 'embs'
    taxonomy_files = list(taxonomy_root_path.glob('*'))

    tag_search_engine = TagEmbeddingSearch(embedding_files=taxonomy_files)
    
    from mail_auto_summrizor.utils.LLM.utils.sumary_utils import summary_job_data

    job_info_cache_path = Path(__file__).parent.parent.parent / 'caches' / 'jobs_info.cache.json'
    with open(job_info_cache_path, 'r', encoding='utf-8') as f:
        job_info_data = json.load(f)

    test_job_data = job_info_data['4433929838']
    result = summary_job_data(test_job_data, tag_search_engine)
    print(result)
