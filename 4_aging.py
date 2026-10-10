# 4_aging.py
# 应收账款账龄分析（假数据练手版）

import pandas as pd
from datetime import datetime, date

# ---------- 1. 生成假数据 ----------
data = [
    ("A公司", "记-001", "2026-09-25", 10000),
    ("A公司", "记-005", "2026-08-20", 5000),
    ("A公司", "记-012", "2026-06-15", 8000),
    ("B公司", "记-003", "2026-09-28", 20000),
    ("B公司", "记-008", "2026-07-10", 15000),
    ("B公司", "记-015", "2026-05-01", 30000),
    ("C公司", "记-020", "2026-09-30", 12000),
    ("C公司", "记-022", "2026-08-05", 18000),
    ("D公司", "记-030", "2026-04-20", 25000),
    ("D公司", "记-031", "2026-03-10", 40000),
]

df = pd.DataFrame(data, columns=["客户名称", "凭证号", "发生日期", "金额"])
df["发生日期"] = pd.to_datetime(df["发生日期"])

# ---------- 2. 算账龄（距今多少天）----------
BASE_DATE = pd.Timestamp("2026-09-30")   # 基准日：审计截止日
df["账龄天数"] = (BASE_DATE - df["发生日期"]).dt.days

# ---------- 3. 分区间 ----------
def bucket(days):
    if days <= 30:
        return "0-30天"
    elif days <= 60:
        return "31-60天"
    elif days <= 90:
        return "61-90天"
    else:
        return "90天以上"

df["账龄区间"] = df["账龄天数"].apply(bucket)

# ---------- 4. 按客户 + 账龄区间 透视 ----------
pivot = df.pivot_table(
    index="客户名称",
    columns="账龄区间",
    values="金额",
    aggfunc="sum",
    fill_value=0,
)

# 确保列的顺序
cols = ["0-30天", "31-60天", "61-90天", "90天以上"]
for c in cols:
    if c not in pivot.columns:
        pivot[c] = 0
pivot = pivot[cols]

# 加合计
pivot["合计"] = pivot.sum(axis=1)

# 最后加一行"总计"
pivot.loc["总计"] = pivot.sum()

print("=== 账龄分析表 ===")
print(pivot)

# ---------- 5. 输出 Excel ----------
pivot.to_excel("账龄分析表.xlsx")
print("\n已生成：账龄分析表.xlsx")
# ---------- 6. 坏账计提测算 ----------
print("\n=== 坏账计提测算 ===")

# 各账龄区间的计提比例
rates = {
    "0-30天": 0.05,
    "31-60天": 0.10,
    "61-90天": 0.30,
    "90天以上": 0.50,
}

# 只取客户行，去掉"总计"行
detail = pivot.drop("总计", errors="ignore")

provision = pd.DataFrame(index=detail.index)
for col, rate in rates.items():
    provision[col + "_计提"] = detail[col] * rate

provision["应计提合计"] = provision.sum(axis=1)

print(provision)

# 汇总应计提总额
total_provision = provision["应计提合计"].sum()
print(f"\n应计提坏账准备总额：{total_provision:,.2f}")

# 输出到 Excel（多个 sheet）
with pd.ExcelWriter("账龄分析表.xlsx") as writer:
    pivot.to_excel(writer, sheet_name="账龄分析")
    provision.to_excel(writer, sheet_name="坏账计提")

print("已更新：账龄分析表.xlsx（含两个 sheet）")