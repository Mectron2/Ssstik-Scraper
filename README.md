# Ssstik-Scraper and a telegram bot for downloading from tik tok. Scraper ported: https://github.com/TobyG74/tiktok-api-dl
Get all the information about videos/photos from TikTok and direct links to them in 1 line of code using the SSSTik.io scraper script
And also an example of a telegram bot for downloading from TikTok :3

## Features
TikTok URL Validation: Ensures the provided URL is in the correct format for TikTok videos or photos.
Content Retrieval: Fetches and parses HTML content from SSSTik.io to extract media details.
Author Information: Extracts and includes author details such as avatar and nickname.
Media Statistics: Provides counts for likes, comments, and shares.
Media Type Detection: Differentiates between photo and video content, providing appropriate direct links.
Error Handling: Robust error handling for invalid URLs and network issues.

## Usage
### Clone the repository:
```
git clone https://github.com/Mectron2/Ssstik-Scraper.git
cd Ssstik-Scraper
```

## Install dependencies:
```
pip install requests beautifulsoup4
```

## Run the script:

### Example:
```
from SsstikScraper import scraper
url = "your_tiktok_url_here"
result = scraper(url)
print(result)
```
### Example of saving video
```
from SsstikScraper import scraper
result = scraper("https://www.tiktok.com/@landon.tech3/video/7355649219438349611")
video_url = result.get("video")
# you can add your own logic for handling request errors
video_request = requests.get(video_url)
with open("video.mp4", "wb") as video:
    video.write(video_request.content)
```
### Example of saving images
```
from SsstikScraper import scraper
result = scraper("https://vm.tiktok.com/ZMMT23rVY/")
images = result.get("images")
# you can add your own logic for handling request errors
for index, image_url in enumerate(images):
    image_request = requests.get(image_url)
    with open(f"{index}.png", "wb") as img:
        img.write(image_request.content)
```
## P.S.
The scraper is ported from here: https://github.com/TobyG74/tiktok-api-dl. I do not own the https://ssstik.io/ service, this code is just a relief for developers, you can always use the original service manually.
