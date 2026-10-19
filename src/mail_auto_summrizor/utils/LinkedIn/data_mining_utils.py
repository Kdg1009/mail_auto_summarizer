import requests
from bs4 import BeautifulSoup
import browser_cookie3

def get_job_data_from_url(url:str):
    cookies = browser_cookie3.chromium(
        domain_name=".linkedin.com"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
            timeout=15
        )
        response.encoding = "utf-8"
        response.raise_for_status()
        
    except requests.exceptions.ConnectionError as e:
        print(f'[ERROR] Network connetion error: {e}')
    
    except requests.exceptions.Timeout:
        print(f'[WARNING] Connection Timeout')

    html = response.text

    return parse_job_html(html)

# ========================================
# get_job_data_from_url 내부에서 사용되는 함수
# ========================================

def parse_job_html(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # 페이지 제목
    page_title = (
        soup.title.get_text(strip=True)
        if soup.title else None
    )

    # 검색창에 표시되는 공고 제목
    title_element = soup.select_one(
        ".search-bar__full-placeholder"
    )
    job_title = (
        title_element.get_text(" ", strip=True)
        if title_element else None
    )

    # 회사 이름
    company_element = soup.select("a.topcard__org-name-link")
    company = company_element[0].text.strip() if company_element else None

    # 공고 상세 설명
    description_element = soup.select_one(
        ".description__text"
    )
    description = (
        description_element.get_text("\n", strip=True)
        if description_element else None
    )

    return {
        "page_title": page_title,
        "job_title": job_title,
        "company": company,
        "description": description,
    }