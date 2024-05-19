import asyncio
import concurrent.futures
from SsstikScraper import scraper
import telebot
import requests
import io

bot = telebot.TeleBot('YOUR_TOKEN_GOES_HERE')

executor = concurrent.futures.ThreadPoolExecutor()

async def async_downloader(url):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, scraper, url)
    return result

def handle_message(message):
    asyncio.run(process_message(message))

async def process_message(message):
    if "https://vm.tiktok.com" in message.text or "https://www.tiktok.com/@" in message.text:
        url = message.text
        result = await async_downloader(url)
        
        if isinstance(result, dict):
            if "images" in result:
                images = result.get("images")
                music = str(result.get("music"))
          
                for i in range(0, len(images), 10):
                    media_group = []
                    for image_url in images[i:i + 10]:
                        image_request = requests.get(image_url)
                        if image_request.status_code in [200, 206]:
                            image_bytes = io.BytesIO(image_request.content)
                            image_bytes.seek(0)
                            media_group.append(telebot.types.InputMediaPhoto(image_bytes))
                        else:
                            bot.send_message(message.chat.id, f"Error loading images: {image_request.status_code}")
                    
                    if media_group:
                        bot.send_media_group(message.chat.id, media_group)

                music_request = requests.get(music)
                music_bytes = io.BytesIO()
                if music_request.status_code in [200, 206]:
                    music_bytes.write(music_request.content)
                    music_bytes.seek(0)
                    bot.send_audio(message.chat.id, music_bytes)
                else:
                    bot.send_message(message.chat.id, f"Audio download error: {music_request.status_code}")

            elif "video" in result:
                video_url = result.get("video")
                music = str(result.get("music"))
                video_request = requests.get(video_url)
                video_bytes = io.BytesIO()
                if video_request.status_code in [200, 206]:
                    video_bytes.write(video_request.content)
                    video_bytes.seek(0)
                    bot.send_video(message.chat.id, video_bytes)
                else:
                    bot.send_message(message.chat.id, f"Video download error: {video_request.status_code}")
                
                music_request = requests.get(music)
                music_bytes = io.BytesIO()
                if music_request.status_code in [200, 206]:
                    music_bytes.write(music_request.content)
                    music_bytes.seek(0)
                    bot.send_audio(message.chat.id, music_bytes)
                else:
                    bot.send_message(message.chat.id, f"Audio download error: {music_request.status_code}")
            else:
                bot.send_message(message.chat.id, "Something went wrong :(")
        else:
            bot.send_message(message.chat.id, str(result))         

bot.message_handler(content_types=["text"])(handle_message)

bot.infinity_polling()
