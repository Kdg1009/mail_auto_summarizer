from mail_auto_summrizor.utils.Gmail import GmailDataHelper, SCOPES
from mail_auto_summrizor.utils.LinkedIn import LinkedInDataHelper
from mail_auto_summrizor.utils.LLM import LLMDataHelper
from mail_auto_summrizor.tags.utils.search_utils import TagEmbeddingSearch

def main():
    tag_searcher = TagEmbeddingSearch()
    LLMDataHelper("qwen3.5:4b-q4_K_M", flush_interval=5)

if __name__ == "__main__":
    main()