import psutil

def create_payload(
        context:str,
        model:str,
        schema:dict,
        system_prompt:str
    ) -> dict:

    memory_info = psutil.virtual_memory()
    flush_model = memory_info.percent > 95.0

    return {
            "model": model,
            "messages":[
                {
                    "role":"system",
                    "content":system_prompt.strip()
                },
                {
                    "role":"user",
                    "content":f'posting:\n{context.strip()}'
                }
            ],
            "format":schema,
            "stream":False,
            "think":False,
            "keep_alive":0 if flush_model else '10m',
            "options":{
                "temperature": 0.0,
                "num_predict": 4096
            }
        }