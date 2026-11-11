import time
import json
import httpx

def record_response_time_cost(ollama_url:str, payload:dict, verbose:bool=True) -> tuple[dict,dict]:
    '''
    Record time spent of llm request to response and return client's response.

    Log:
    - total time duration
    - model loading time duration
    - handling prompt time duration
    - generating response time duration
    
    Return:
    - content of llm request.
    '''

    start = time.perf_counter()

    with httpx.Client(timeout=600.0) as client:
        response = client.post(ollama_url, json=payload)

    elapsed = time.perf_counter() - start

    response.raise_for_status()

    data = response.json()

    if verbose:
        print(f"\n요청 소요 시간: {elapsed:.2f}초")
        print(f"모델 로딩 시간: {data.get('load_duration', 0) / 1e9:.2f}초")
        print(f"프롬프트 처리 시간: {data.get('prompt_eval_duration', 0) / 1e9:.2f}초")
        print(f"응답 생성 시간: {data.get('eval_duration', 0) / 1e9:.2f}초")

    content = data["message"]["content"]
    try:
        result = json.loads(content)

    except json.JSONDecodeError as e:
        print("\n[JSON PARSE ERROR]")
        print(f"Error: {e}")
        print(f"Line: {e.lineno}, Column: {e.colno}")
        print(f"Position: {e.pos}")

        lines = content.splitlines()

        start = max(0, e.lineno - 4)
        end = min(len(lines), e.lineno + 3)

        print("\n[RAW RESPONSE AROUND ERROR]")

        for i in range(start, end):
            print(f"{i + 1}: {lines[i]}")

        print("\n[RAW RESPONSE]")
        print(repr(content))

        raise

    time_log = {
        "Total time": elapsed,
        "Load model": data.get("load_duration", 0) / 1e9,
        "Prompt handle": data.get("prompt_eval_duration", 0) / 1e9,
        "Generate response": data.get("eval_duration", 0) / 1e9,
    }

    return result, time_log

# ==============================
# LLM Request function
# ==============================

from mail_auto_summrizor.utils.LLM.utils.response_styles import record_response_time_cost
from mail_auto_summrizor.tags.utils.search_utils import TagEmbeddingSearch
from mail_auto_summrizor.utils.LLM.data_interface_manage.create_payloads_utils import (create_payload)
from mail_auto_summrizor.utils.LLM.data_interface_manage.schemas import make_evidence_extraction_schema
import json

OLLAMA_URL = "http://localhost:11434/api/chat"

def request_LLM_to_make_tag(
        model:str,
        source_context:str,
        evidence_extraction_prompt:str,
        tag_selection_prompt:str,
        target_schema:dict,
        tag_searcher:TagEmbeddingSearch,
        target_subject:list[str],
        verbose:bool=True
    ) -> tuple[dict,dict]:
    '''
    Pipeline:
    1. Extract verbatim evidence relevant to requested taxonomy subjects.
    2. Retrieve candidate tags with semantic search.
    3. Classify and summarize the evidence using only valid candidate IDs.
    '''

    if not source_context.strip():
        raise ValueError("[ERROR] Job description is empty")

    # Extract evidence for 2nd LLM to make tags.
    extraction_schema = make_evidence_extraction_schema(target_subject)
    extraction_payload = create_payload(source_context, model, extraction_schema, evidence_extraction_prompt)
    extraction_result, extraction_time_log = record_response_time_cost(OLLAMA_URL,extraction_payload, verbose)

    if not isinstance(extraction_result, str):
        raise TypeError(f"[ERROR] Extraction result must be a string. Extraction result: {extraction_result}")
    if not extraction_result.strip():
        raise ValueError("[ERROR] Extraction result is empty.")

    # Search relative tags
    tags = tag_searcher.search(extraction_result, top_k=5, subject=target_subject)
    tags_json = json.dumps(tags, ensure_ascii=False, indent=2) # Convert to LLM preferred readable form.

    # Request LLM to make tags
    analysis_payload = create_payload(extraction_result,model,target_schema,tag_selection_prompt)
    result, analysis_time_log = record_response_time_cost(OLLAMA_URL, analysis_payload,verbose)

    time_log = {
        "Extraction": extraction_time_log,
        "Analysis": analysis_time_log,
        "Total": {
            key: extraction_time_log[key] + analysis_time_log[key]
            for key in extraction_time_log
        }
    }
    
    return (result, time_log)