import requests
from bs4 import BeautifulSoup
import re
import time

SSSTIK_URL = "https://ssstik.io"
SSSTIK_API = f"{SSSTIK_URL}/abc?url=dl"
TIKTOK_URL_REGEX = re.compile(r'https://(vm\.tiktok\.com/[\w-]+|www\.tiktok\.com/@[\w.-]+/(photo|video)/\d+)')

class SSSTikFetchTT:
    def __init__(self, status: str, result: str = None, message: str = None):
        self.status = status
        self.result = result
        self.message = message

class Author:
    def __init__(self, avatar: str, nickname: str):
        self.avatar = avatar
        self.nickname = nickname

class Statistics:
    def __init__(self, like_count: str, comment_count: str, share_count: str):
        self.like_count = like_count
        self.comment_count = comment_count
        self.share_count = share_count

class SSSTikResponse:
    def __init__(self, status: str, result: dict = None, message: str = None):
        self.status = status
        self.result = result
        self.message = message

def fetch_tt() -> SSSTikFetchTT:
    try:
        response = requests.get(SSSTIK_URL, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"})
        response.raise_for_status()
        match = re.search(r's_tt\s*=\s*["\']([^"\']+)["\']', response.text)
        if match:
            value = match.group(1)
            return SSSTikFetchTT(status="success", result=value)
        else:
            return SSSTikFetchTT(status="error", message="Failed to get the request form!")
    except requests.RequestException as e:
        return SSSTikFetchTT(status="error", message=str(e))

def ssstik(url: str) -> SSSTikResponse:
    if not TIKTOK_URL_REGEX.match(url):
        return SSSTikResponse(status="error", message="Invalid Tiktok URL. Make sure your url is correct!")

    tt = fetch_tt()
    if tt.status != "success":
        return SSSTikResponse(status="error", message=tt.message)

    while True:
        try:
            response = requests.post(SSSTIK_API, headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": SSSTIK_URL,
                "Referer": f"{SSSTIK_URL}/en",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"
            }, data={
                "id": url,
                "locale": "en",
                "tt": tt.result
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            error_message_element = soup.select_one("div.panel.notification")
            if error_message_element:
                return SSSTikResponse(status="error", message="No content available for this URL")

            desc_element = soup.select_one("p.maintext")
            if desc_element:
                break

            time.sleep(0.2)
        except requests.RequestException as e:
            return SSSTikResponse(status="error", message=str(e))

    desc = desc_element.get_text(strip=True)

    author_element = soup.select_one("img.result_author")
    avatar = author_element["src"] if author_element else ""

    nickname_element = soup.select_one("h2")
    nickname = nickname_element.get_text(strip=True) if nickname_element else ""

    author = Author(avatar=avatar, nickname=nickname)

    like_count_element = soup.select_one("#trending-actions > .justify-content-start")
    comment_count_element = soup.select_one("#trending-actions > .justify-content-center")
    share_count_element = soup.select_one("#trending-actions > .justify-content-end")

    like_count = like_count_element.get_text(strip=True) if like_count_element else "0"
    comment_count = comment_count_element.get_text(strip=True) if comment_count_element else "0"
    share_count = share_count_element.get_text(strip=True) if share_count_element else "0"

    statistics = Statistics(
        like_count=like_count,
        comment_count=comment_count,
        share_count=share_count
    )

    images = [img["href"] for img in soup.select("ul.splide__list > li a")]

    if images:
        result = {
            "type": "image",
            "desc": desc,
            "author": author,
            "statistics": statistics,
            "images": images,
            "music": soup.select_one("a.music")["href"]
        }
    else:
        result = {
            "type": "video",
            "desc": desc,
            "author": author,
            "statistics": statistics,
            "video": soup.select_one("a.without_watermark")["href"],
            "music": soup.select_one("a.music")["href"]
        }
    return SSSTikResponse(status="success", result=result)

def scraper(url):
    response = ssstik(url)
    if response.status == "success":
        return response.result
    else:
        return response.message
