import re
import unicodedata

def rule_based_removal(description:str, **kwargs) -> str:

    description = unicodedata.normalize("NFKC", description)

    # 1. remove \nShow more\nShow less
    processed = re.sub(
        r"(?im)^[ \t]*Show (?:more|less)[ \t]*$",
        "",
        description
    )

    # 2. remove repeated - or _
    processed = re.sub(
        r"(?m)^[ \t]*[-–—_]{2,}[ \t]*$",
        "",
        processed
    )

    # 3. remove emojies
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "\U00002700-\U000027BF"
        "\U00002600-\U000026FF"
        "]+",
        flags=re.UNICODE
    )
    processed = emoji_pattern.sub("", processed)

    # 4. remove meaningless space, tabs, enters
    processed = re.sub(r"[ \t]+", " ", processed)
    processed = re.sub(r" *\n *", "\n", processed)
    processed = re.sub(r"\n{2,}", "\n", processed)
    processed = re.sub(r"([,\.])\s+", r"\1", processed)

    return processed

# ======================================================
# experimental filters
# ======================================================

def remove_company_name(description:str, **kwargs) -> str:
    '''
    Replace company name like Intel or NVIDIA into `company`.

    Anticipate prompt optimization in long conpany name.
    '''
    company_name = kwargs.get("company","")
    
    if not company_name.strip():
        return description

    pattern = re.compile(re.escape(company_name.strip()), re.IGNORECASE)
    return pattern.sub("company", description)

PREPROCESS_PIPELINE = [
    rule_based_removal,
    remove_company_name
]