# 8_gen_ar.py
# 生成一份假的应收账款明细表（练手用）
# 字段：客户名称、凭证号、发生日期、金额

import random
from datetime import date, timedelta

import pandas as pd

random.seed(42)  # 固定种子，结果可复现

START = date(2026, 1, 1)
END = date(2026, 9, 30)
TOTAL_DAYS = (END - START).days  # 272 天

# 客户A 到 客户T，共 20 个客户
customers = [f"客户{chr(ord('A') + i)}" for i in range(20)]

rows = []
voucher_no = 1
for cust in customers:
    n = random.randint(1, 5)  # 每个客户 1-5 笔
    for _ in range(n):
        d = START + timedelta(days=random.randint(0, TOTAL_DAYS))
        rows.append({
            "客户名称": cust,
            "凭证号": f"记-{voucher_no:03d}",
            "发生日期": d.strftime("%Y-%m-%d"),
            "金额": round(random.uniform(5000, 80000), 2),
        })
        voucher_no += 1

df = pd.DataFrame(rows)
df.to_excel("应收明细_假数据.xlsx", index=False)

print("已生成：应收明细_假数据.xlsx")
print(f"共 {len(df)} 行，{df['客户名称'].nunique()} 个客户")
print(df.head(10))
