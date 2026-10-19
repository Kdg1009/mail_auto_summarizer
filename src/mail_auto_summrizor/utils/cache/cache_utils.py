import json

def save_cache(cache, path):
    '''
    We need to save data in cache because Linkedin website response with `429 Client Error: Too Many Requests`
    when too many requests happens in time duration.

    I don't know their threshold for this, but when i apply 2 sec sleep and save every cache, it didn't happen.
    '''
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(cache, file, ensure_ascii=False, indent=4)
