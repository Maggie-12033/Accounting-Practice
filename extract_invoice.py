# extract_invoice.py
# 用正则提取发票号码

import re

# 假设这是 OCR 识别出来的乱糟糟的文本
ocr_text = """
增值税专用发票
购买方：某某科技有限公司
金额：￥15,000.00
发票代码：044001900111
发票号码：12345678
开票日期：2026年10月15日
"""

# 正则表达式：寻找“发票号码：”后面跟着的连续数字
# \d+ 表示连续的数字
pattern = r"发票号码：(\d+)"

# 查找
match = re.search(pattern, ocr_text)

if match:
    invoice_no = match.group(1) # 拿到括号里的数字
    print(f"成功提取！发票号码是：{invoice_no}")
else:
    print("没找到发票号码")