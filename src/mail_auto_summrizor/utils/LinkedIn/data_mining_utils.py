import requests
from bs4 import BeautifulSoup
import browser_cookie3

def get_cookie(browser:str):
    '''
    From chrome v.155, there is a change in cookie encryption and browser_cookie3
    cannot decode them, so you need to get cookies manually.

    1. Install 'editThisCookie' in chrome.
    2. Get cookies from linkedin job page in 'Netscape Http Cookie File`
    3. Copy and paste them at SECRETS_DIR/'linkedin_chrome_cookies.txt'
    '''
    
    if browser == 'chromium':
        return browser_cookie3.chromium(
            domain_name=".linkedin.com"
        )
    elif browser == 'chrome':
        from http.cookiejar import MozillaCookieJar
        from mail_auto_summrizor.utils.paths import SECRETS_DIR

        cookies_path = SECRETS_DIR/"linkedin_chrome_cookies.txt"

        cookies = MozillaCookieJar(str(cookies_path))
        cookies.load(ignore_discard=True, ignore_expires=True)

        return cookies
    else:
        raise ValueError(
            f"[ERROR] Unsupported browser: {browser}"
        )

def get_job_data_from_url(url:str, browser:str='chromium'):
    try:
        cookies = get_cookie(browser)
        
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        with requests.Session() as session:
            session.cookies.update(cookies)

            response = session.get(
                url,
                headers=headers,
                timeout=15
            )

            response.raise_for_status()
            response.encoding = 'utf-8'
            html = response.text

        return parse_job_html(html)
        
    except requests.exceptions.ConnectionError as e:
        print(f'[ERROR] Network connetion error: {e}')
    
    except requests.exceptions.Timeout:
        print(f'[WARNING] Connection Timeout')

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error: {e}")

    except FileNotFoundError as e:
        print(f"[ERROR] Cookie file not found: {e}")

    except browser_cookie3.BrowserCookieError as e:
        print(f"[ERROR] Failed to load browser cookies: {e}")

    return None

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