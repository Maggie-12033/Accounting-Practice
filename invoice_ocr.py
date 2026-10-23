# invoice_ocr.py
# 用 Pillow 生成一张带有文字的图片，模拟“发票扫描件”

from PIL import Image, ImageDraw, ImageFont
import os

# 如果没装 Pillow，终端跑：pip install Pillow
# 如果后面要 OCR，还要跑：pip install pytesseract

# 创建一张白底图片
img = Image.new('RGB', (800, 400), color='white')
d = ImageDraw.Draw(img)

# 在图片上“写”上发票内容
# 这里为了演示，我们画一些无意义的字和我们要提取的发票号码
text_lines = [
    "增值税专用发票",
    "购买方：某某科技有限公司",
    "金额：￥15,000.00",
    "发票代码：044001900111",
    "发票号码：12345678",
    "开票日期：2026年10月15日"
]

y_offset = 50
for line in text_lines:
    d.text((50, y_offset), line, fill='black')
    y_offset += 40

# 保存为图片
img.save("发票扫描件_假数据.png")
print("已生成：发票扫描件_假数据.png")