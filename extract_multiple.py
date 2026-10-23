import re

ocr_text = """
购买方: 某某科技有限公司
发票代码: 044001900111 发票号码: 12345678
开票日期: 2026年10月15日 金额: ￥15,000.00
"""

print("正在提取...")

# 1. 提取发票号码（找"发票号码"后面的数字）
number = re.search(r"发票号码[:\s]*(\d+)", ocr_text)

# 2. 提取金额（找"金额"后面的数字，可能有逗号和小数点）
amount = re.search(r"金额[:\s]*￥?([\d,]+\.\d{2})", ocr_text)

# 3. 提取日期（找 XXXX年XX月XX日）
date = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", ocr_text)

print("-" * 30)
if number: print(f"发票号码：{number.group(1)}")
if amount: print(f"金额：{amount.group(1)}")
if date: print(f"日期：{date.group(1)}")