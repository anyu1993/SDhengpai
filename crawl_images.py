#!/usr/bin/env python3
"""
爬取磁分离机相关产品图片
"""
import os
import asyncio
from pathlib import Path
from scrapling.spiders import Spider, Request, Response

OUTPUT_DIR = Path(__file__).parent
IMAGE_DIR = OUTPUT_DIR / "downloaded_images"
IMAGE_DIR.mkdir(exist_ok=True)

class MagneticSeparatorSpider(Spider):
    name = "magnetic-separator-images"
    
    # 目标网站列表（水处理设备公司）
    start_urls = [
        # 青岛金牌机械 - 磁分离设备
        "https://www.hbjnhb.com/",
        # 海普欧环保
        "https://www.cnhpo.com/",
        # 搜好货网 - 磁分离设备
        "https://www.912688.com/",
        # 环保设备商城
        "https://www.hbzhan.com/",
    ]
    
    concurrent_requests = 3
    download_delay = 2
    
    def parse(self, response: Response):
        # 提取图片链接
        if response.css('img'):
            for img in response.css('img'):
                src = img.attrib.get('src') or img.attrib.get('data-src') or ''
                alt = img.attrib.get('alt', '')
                
                # 筛选与磁分离相关的图片
                keywords = ['磁分离', '磁混凝', '污水处理', '水处理', 'magnetic', 'separator', 'wastewater']
                if any(k.lower() in (src + alt).lower() for k in keywords):
                    print(f"Found: {src} (alt: {alt})")
                    yield response.follow(src, self.download_image)
        
        # 跟随产品列表页链接
        for link in response.css('a::attr(href)').getall():
            if any(k in link.lower() for k in ['chanpin', 'product', 'cili', 'magnetic']):
                yield response.follow(link)

    def download_image(self, response: Response):
        content_type = response.headers.get('content-type', b'').decode()
        if 'image' not in content_type:
            return
            
        url = response.url
        filename = url.split('/')[-1].split('?')[0]
        if not filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            filename += '.jpg'
        
        filepath = IMAGE_DIR / filename
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filepath}")

if __name__ == "__main__":
    result = MagneticSeparatorSpider(crawldir=f"{IMAGE_DIR}/crawl_data").start()
    print(f"\nDone! Downloaded images to: {IMAGE_DIR}")
