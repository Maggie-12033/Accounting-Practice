import pandas as pd
import re

# 模拟一堆乱七八糟的凭证摘要
data = {
    "凭证号": ["记-001", "记-002", "记-003", "记-004", "记-005"],
    "摘要": [
        "付A公司3月货款 12000元",
        "支付B公司货款",
        "付C公司2月份款 3400",
        "支付D公司货款",
        "交电费 850"
    ]
}
df = pd.DataFrame(data)

# 写正则：提取“付”或“支付”后面的 公司名称（到“货款”或“款”为止）
# [付|支付] 表示 付 或 支付
# (.*?) 表示 非贪婪捕获任意字符
# 公司|货款 表示 遇到“公司”或“货款”就停
def get_company(text):
    match = re.search(r"(?:付|支付)(.*?)(?:公司|货款)", text)
    if match:
        return match.group(1).strip() + "公司"
    return "未识别"

df["识别出的客户"] = df["摘要"].apply(get_company)

print(df)