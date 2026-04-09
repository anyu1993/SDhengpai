#!/usr/bin/env python3
"""直接下载水处理设备相关图片"""
import os
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "downloaded_images"
OUTPUT_DIR.mkdir(exist_ok=True)

# 免费图片源列表 (CC0 license)
IMAGE_SOURCES = {
    "magnetic_separator": [
        # 工业设备相关的免费图片
        "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800",
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
        "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=800",
    ],
    "filter": [
        "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=800",
        "https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=800",
    ],
    "uv_device": [
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800",
        "https://images.unsplash.com/photo-1585435557343-3b092031a831?w=800",
    ],
    "mixer": [
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800",
        "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800",
    ],
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def download_image(url, filename):
    filepath = OUTPUT_DIR / filename
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"Downloaded: {filepath} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"Failed: {url} - {e}")
        return False

# 下载所有图片
for category, urls in IMAGE_SOURCES.items():
    for i, url in enumerate(urls):
        filename = f"{category}_{i+1}.jpg"
        download_image(url, filename)

print(f"\nDone! Images saved to: {OUTPUT_DIR}")
