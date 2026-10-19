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
    result = json.loads(content)

    time_log = {
        "Total time": f"{elapsed:.2f}sec",
        "Load model": f"{data.get('load_duration', 0) / 1e9:.2f}sec",
        "Prompt handle": f"{data.get('prompt_eval_duration', 0) / 1e9:.2f}sec",
        "Generate response": f"{data.get('eval_duration', 0) / 1e9:.2f}sec"
    }

    return result, time_log