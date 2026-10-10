# 1_make_data.py
# 生成一个假的凭证表 Excel，用来练手

import pandas as pd
import random

random.seed(42)

accounts = [
    ("1001", "库存现金"),
    ("1002", "银行存款"),
    ("1122", "应收账款"),
    ("1405", "库存商品"),
    ("2202", "应付账款"),
    ("6001", "主营业务收入"),
    ("6401", "主营业务成本"),
    ("6602", "管理费用"),
]

rows = []
for i in range(1, 31):
    code, name = random.choice(accounts)
    if random.random() < 0.5:
        debit = round(random.uniform(1000, 50000), 2)
        credit = 0
    else:
        debit = 0
        credit = round(random.uniform(1000, 50000), 2)
    rows.append({
        "凭证号": f"记-{i:03d}",
        "日期": f"2026-09-{random.randint(1, 28):02d}",
        "科目代码": code,
        "科目名称": name,
        "摘要": "测试数据",
        "借方金额": debit,
        "贷方金额": credit,
    })

df = pd.DataFrame(rows)
df.to_excel("凭证表_假数据.xlsx", index=False)

print("已生成：凭证表_假数据.xlsx")
print(f"共 {len(df)} 行")
print(df.head())