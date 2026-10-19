"""
Later, i need to cache labels and filters that currently applied in Gmail. And update
- create_filters
- deleta_filter
- get_label_by_name
- create_label
"""

def get_filters(service):
    result = service.users().settings().filters().list(
        userId="me"
    ).execute()

    return result.get("filter", [])

def create_filters(service):
    """
    Create Gmail filters from JSON files.

    Notice:
        Only one label is supported for one filter.
    """

    from mail_auto_summrizor.utils.paths import FILTER_SETTINGS_DIR
    import json

    filter_ids = []

    for filter_file in FILTER_SETTINGS_DIR.glob("*.json"):
        try:
            with open(filter_file, 'r', encoding="utf-8") as f:
                filter_content = json.load(f)

                action = filter_content["action"]
                label_names = action.pop("addLabelNames",[])
                label_ids = []

                for name in label_names:
                    label_id = get_label_by_name(service, name)

                    if label_id is None:
                        raise ValueError(
                            f"[ERROR] Invalid label found in {filter_file}. Invalid label: {name}"
                        )

                    label_ids.append(label_id)

                action["addLabelIds"] = label_ids

                filter_id = _create_filter(service, filter_content)

                if filter_id is not None:
                    filter_ids.append(filter_id)

        except Exception as error:
            print(f'[ERROR] {filter_file}: {error}')
            continue
    
    return filter_ids

def _create_filter(service, filter_content):
    """
    Create a filter.
    Returns:
        str | None: Created filter ID, or None if creation fails.
    """
    from googleapiclient.errors import HttpError

    try:
        result = (
            service.users()
                .settings()
                .filters()
                .create(userId="me", body=filter_content)
                .execute()
        )

    except HttpError as error:
        print(f'[ERROR] {error}')
        return None

    return result.get("id")

def delete_filter(service, filter_id):
    from googleapiclient.errors import HttpError
    
    try:
        (
            service.users()
                .settings()
                .filters()
                .delete(userId="me", id=filter_id)
                .execute()
        )
        return True

    except HttpError as error:
        print(f'[ERROR] Exception was raised while deleting {filter_id} {error}')
        return False

# ==================================================================
# Label utils
# ==================================================================

from mail_auto_summrizor.utils.paths import CACHE_DIR
import json

LABEL_CACHE = CACHE_DIR / "labels.cache.json"

def get_labels_from_gmail(service):
    '''
    This function updates labels.cache.json
    '''
    
    result = (
        service.users()
            .labels()
            .list(userId="me")
            .execute()
    )

    cache_data = {
        label["name"]: label["id"]
        for label in result.get("labels", [])
    }

    with open(LABEL_CACHE, 'w', encoding="utf-8") as output_file:
        json.dump(cache_data, output_file, ensure_ascii=False, indent=4)

    return cache_data


def get_label_by_name(service, label_name):

    if not LABEL_CACHE.exists():
        print('[INFO] Creating label cache...')
        get_labels_from_gmail(service)
        print('[INFO] Finish creating label cache')

    with open(LABEL_CACHE, "r") as f:
        labels = json.load(f)

    return labels.get(label_name)

def create_label(service, label_name:str):

    if get_label_by_name(service, label_name) is not None:
        return

    body = {"name":label_name}

    result = (
        service.users()
            .labels()
            .create(userId="me", body=body)
            .execute()
    )

    # Update cache
    with open(LABEL_CACHE, "r", encoding="utf-8") as f:
        labels = json.load(f)

    labels[label_name] = result["id"]

    with open(LABEL_CACHE, "w", encoding="utf-8") as f:
        json.dump(labels, f, ensure_ascii=False, indent=4)


def delete_label(service, label_name:str):

    label_id = get_label_by_name(service, label_name)

    if label_id is None:
        return

    service.users().labels().delete(
        userId="me",
        id=label_id
    ).execute()

    with open(LABEL_CACHE, 'r') as f:
        labels = json.load(f)

    del labels[label_name]

    with open(LABEL_CACHE, "w") as f:
        json.dump(labels, f, ensure_ascii=False, indent=4)