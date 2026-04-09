#!/usr/bin/env python3
"""生成专业的产品占位图"""
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
SIZE = (800, 600)

def create_placeholder(name_cn, name_en, icon_type, color_scheme, filename):
    """创建专业的产品占位图"""
    # 颜色配置
    bg_color = color_scheme['bg']      # 深色背景
    accent_color = color_scheme['accent']  # 主色调
    text_color = '#FFFFFF'
    subtext_color = '#94A5C7'
    
    # 创建图像
    img = Image.new('RGB', SIZE, bg_color)
    draw = ImageDraw.Draw(img)
    
    # 绘制科技感背景网格
    for i in range(0, SIZE[0], 50):
        draw.line([(i, 0), (i, SIZE[1])], fill=(0, 119, 255, 15))
    for i in range(0, SIZE[1], 50):
        draw.line([(0, i), (SIZE[0], i)], fill=(0, 119, 255, 15))
    
    # 绘制渐变圆形光晕
    for radius in [200, 150, 100]:
        alpha = int(255 * 0.05 * (1 - radius/200))
        draw.ellipse(
            [(SIZE[0]//2 - radius, SIZE[1]//2 - radius),
             (SIZE[0]//2 + radius, SIZE[1]//2 + radius)],
            fill=(0, 119, 255, alpha)
        )
    
    # 绘制图标区域背景
    icon_bg_radius = 80
    draw.ellipse(
        [(SIZE[0]//2 - icon_bg_radius, SIZE[1]//2 - icon_bg_radius - 40),
         (SIZE[0]//2 + icon_bg_radius, SIZE[1]//2 + icon_bg_radius - 40)],
        fill=(0, 119, 255, 30)
    )
    
    # 绘制图标 (简单几何形状表示不同设备)
    cx, cy = SIZE[0]//2, SIZE[1]//2 - 40
    
    if icon_type == 'magnet':
        # 磁分离机 - 磁铁形状
        draw.arc([cx-50, cy-40, cx-10, cy+20], 0, 180, fill=accent_color, width=8)
        draw.arc([cx+10, cy-40, cx+50, cy+20], 0, 180, fill=accent_color, width=8)
        draw.rectangle([cx-50, cy-40, cx+50, cy-20], fill=accent_color)
        draw.rectangle([cx-50, cy+10, cx+50, cy+30], fill=accent_color)
    elif icon_type == 'filter':
        # 高精度过滤器 - 漏斗形状
        draw.polygon([(cx-40, cy-50), (cx+40, cy-50), (cx+20, cy+30), (cx-20, cy+30)], fill=accent_color)
        draw.ellipse([cx-50, cy+20, cx+50, cy+60], fill=accent_color)
        for i in range(3):
            y = cy - 30 + i * 25
            draw.ellipse([cx-30+i*5, y, cx+30-i*5, y+8], outline='#FFFFFF', width=2)
    elif icon_type == 'uv':
        # 紫外消毒 - 灯泡+光芒
        draw.ellipse([cx-30, cy-50, cx+30, cy-10], fill=accent_color)
        draw.rectangle([cx-15, cy-10, cx+15, cy+30], fill=accent_color)
        for angle in range(0, 360, 45):
            import math
            x2 = cx + int(55 * math.cos(math.radians(angle)))
            y2 = cy - 30 + int(55 * math.sin(math.radians(angle)))
            draw.line([(cx, cy-30), (x2, y2)], fill=accent_color, width=3)
    elif icon_type == 'mixer':
        # 搅拌器 - 搅拌桨叶
        draw.rectangle([cx-10, cy-60, cx+10, cy+50], fill=accent_color)
        draw.ellipse([cx-40, cy-20, cx, cy+10], fill=accent_color)
        draw.ellipse([cx, cy-10, cx+40, cy+20], fill=accent_color)
        draw.ellipse([cx-35, cy+20, cx, cy+45], fill=accent_color)
        draw.ellipse([cx, cy+25, cx+35, cy+50], fill=accent_color)
    elif icon_type == 'shear':
        # 高速剪切机 - 旋转刀片
        draw.ellipse([cx-40, cy-40, cx+40, cy+40], outline=accent_color, width=6)
        for i in range(6):
            import math
            angle = i * 60
            x1 = cx + int(15 * math.cos(math.radians(angle)))
            y1 = cy + int(15 * math.sin(math.radians(angle)))
            x2 = cx + int(40 * math.cos(math.radians(angle)))
            y2 = cy + int(40 * math.sin(math.radians(angle)))
            draw.line([(x1, y1), (x2, y2)], fill=accent_color, width=4)
        draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill=accent_color)
    elif icon_type == 'floc':
        # 磁混凝 - 多层结构
        draw.rectangle([cx-60, cy-50, cx+60, cy+50], outline=accent_color, width=4)
        for i in range(4):
            y = cy - 35 + i * 20
            draw.ellipse([cx-45+i*3, y, cx+45-i*3, y+12], outline='#FFFFFF', width=2)
    
    # 绘制文字
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 20)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 产品名称
    bbox = draw.textbbox((0, 0), name_cn, font=font_large)
    text_width = bbox[2] - bbox[0]
    draw.text((SIZE[0]//2 - text_width//2, SIZE[1]//2 + 80), name_cn, fill=text_color, font=font_large)
    
    # 英文名
    bbox = draw.textbbox((0, 0), name_en, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text((SIZE[0]//2 - text_width//2, SIZE[1]//2 + 125), name_en, fill=subtext_color, font=font_small)
    
    # 添加"产品图片"标签
    draw.rounded_rectangle([SIZE[0]//2-60, SIZE[1]-60, SIZE[0]//2+60, SIZE[1]-30], radius=10, fill=(0, 119, 255, 60))
    draw.text((SIZE[0]//2-40, SIZE[1]-55), "示意图片", fill='#94A5C7', font=font_small)
    
    # 保存
    filepath = OUTPUT_DIR / filename
    img.save(filepath, 'JPEG', quality=90)
    print(f"Created: {filepath}")

# 定义6个产品的配置
products = [
    {
        'name_cn': '磁分离机',
        'name_en': 'Magnetic Separator',
        'icon_type': 'magnet',
        'color_scheme': {'bg': '#0a0f1a', 'accent': '#0077FF'},
        'filename': 'product_magnetic_separator.jpg'
    },
    {
        'name_cn': '高精度过滤器',
        'name_en': 'High Precision Filter',
        'icon_type': 'filter',
        'color_scheme': {'bg': '#0a0f1a', 'accent': '#00C7BE'},
        'filename': 'product_high_precision_filter.jpg'
    },
    {
        'name_cn': '紫外消毒模块',
        'name_en': 'UV Disinfection Module',
        'icon_type': 'uv',
        'color_scheme': {'bg': '#0a0f1a', 'accent': '#5856D6'},
        'filename': 'product_uv_disinfection.jpg'
    },
    {
        'name_cn': '反应池搅拌器',
        'name_en': 'Reactor Agitator',
        'icon_type': 'mixer',
        'color_scheme': {'bg': '#0a0f1a', 'accent': '#3B82F6'},
        'filename': 'product_reactor_agitator.jpg'
    },
    {
        'name_cn': '高速剪切机',
        'name_en': 'High Shear Machine',
        'icon_type': 'shear',
        'color_scheme': {'bg': '#0a0f1a', 'accent': '#F97316'},
        'filename': 'product_high_shear_machine.jpg'
    },
    {
        'name_cn': '磁混凝设备',
        'name_en': 'Magnetic Flocculation',
        'icon_type': 'floc',
        'color_scheme': {'bg': '#0a0f1a', 'accent': '#A855F7'},
        'filename': 'product_magnetic_flocculation.jpg'
    },
]

# 生成所有产品图片
for product in products:
    create_placeholder(**product)

print("\nAll product placeholder images created!")
