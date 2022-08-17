# coding: utf-8
import aiohttp
import os
import time

download_dir = "/data/download"

async def download_image(image_url, filename=""):
    downloaded_file = os.path.join(download_dir, filename if filename else str(time.time()))
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            binary_content = await resp.read()
            with open(downloaded_file, "wb") as f:
                f.write(binary_content)
    return downloaded_file