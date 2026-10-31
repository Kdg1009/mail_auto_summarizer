from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError,
)

from mail_auto_summrizor.utils.paths import SECRETS_DIR

LINKEDIN_PROFILE_DIR = SECRETS_DIR / "linkedin_playwright_profile"

WORK_MODES = [
    "대면근무",
    "재택대면혼합근무",
    "재택근무",
]
EMPLOY_TYPES = [
    "계약직",
    "프리랜서/개인사업자",
    "파트타임",
    "정규직",
    "인턴십",
    "수습",
    "프리랜서"
]

def extract_job_types(soup):
    found_texts = set()
    
    for link in soup.select('a[href*="/jobs/view/"]'):
        for span in link.select("span"):
            text = span.get_text(strip=True)
            if text:
                found_texts.add(text)
                
    work_mode = next(
        (mode for mode in WORK_MODES if mode in found_texts),
        None,
    )
    
    employment_type = next(
        (em_type for em_type in EMPLOY_TYPES if em_type in found_texts),
        None,
    )
    
    return {
        'work_mode':work_mode,
        'employment_type':employment_type
    }

def get_job_data_from_url(url:str, headless:bool=True):
    '''
    Open recruiting page and extract informations using playwright

    Returns:
        recruit_data: Returns dict if success, else None
    '''

    LINKEDIN_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(LINKEDIN_PROFILE_DIR),
                headless=headless,
                executable_path="/usr/bin/chromium",
                viewport={"width":1280, "height": 900}
            )

            try:
                page = context.new_page()

                response = page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )

                if response is not None and response.status >= 400:
                    print(f'[ERROR] HTTP error: {response.status}')
                    return None

                current_url = page.url.lower()

                if "/login" in current_url or "/checkpoint" in current_url:
                    print(f'[WARNING] You need to login to LinkedIn or need additional authentication.')

                    try:
                        page.wait_for_url(
                            lambda url: (
                                "linkedin.com" in str(url).lower()
                                and "/login" not in str(url).lower()
                                and "/checkpoint" not in str(url).lower()
                            ),
                            timeout=300000
                        )
                    except PlaywrightTimeoutError:
                        print('[ERROR] Login timeout')
                        return None

                    response = page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000,
                    )
                    if response is not None and response.status >= 400:
                        print(f'[ERROR] HTTP error: {response.status}')
                        return None

                # 1. Wait for job details to be loaded.
                about = page.locator(
                    '[id^="JobDetails_AboutTheJob_"]'
                )
                about.wait_for(state='visible', timeout=30000)
                description_box = about.get_by_test_id("expandable-text-box")
                description_box.wait_for(state='visible', timeout=30000)

                # wait until description page loads
                page.wait_for_function(
                    '''
                    () => {
                        const container = document.querySelector(
                            '[id^="JobDetails_AboutTheJob_"]'
                        );

                        const box = container?.querySelector(
                            '[data-testid="expandable-text-box"]'
                        );

                        return box && box.innerText.trim().length > 100;
                    }
                    ''',
                    timeout=30000,
                )
                # 2. Unfold whole job description.
                more_button = description_box.get_by_test_id(
                    "expandable-text-button"
                )

                if (more_button.count() > 0 and more_button.first.is_visible()):
                    more_button.first.click()
                    page.wait_for_timeout(300)

                job_description = description_box.inner_text().strip()

                # 3. Get final HTML page
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                page_title = (
                    soup.title.get_text(strip=True)
                    if soup.title else None
                )

                company = None
                job_title = None
                if page_title:
                    parts = page_title.split("|")
                    cleaned_parts = [item.strip() for item in parts]
                    job_title = cleaned_parts[0]
                    company = cleaned_parts[1]   
                    
                job_types = extract_job_types(soup)

                return {
                    'page_title':page_title,
                    'job_title':job_title,
                    'company':company,
                    'work_mode': job_types['work_mode'],
                    'employment_type': job_types['employment_type'],
                    'description':job_description
                }
            finally:
                context.close()
    except PlaywrightTimeoutError as e:
        print(f'[WARNING] Page load timeout: {e}')

    except PlaywrightError as e:
        print(f'[ERROR] playwright error: {e}')

    return None