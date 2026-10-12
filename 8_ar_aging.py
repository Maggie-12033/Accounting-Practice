# 8_ar_aging.py
# 应收账款账龄分析（读取 应收明细_假数据.xlsx）
# 基准日：2026-09-30
# 账龄区间：0-30天 / 31-60天 / 61-90天 / 90天以上
# 坏账计提比例：5% / 10% / 30% / 50%

import pandas as pd

BASE_DATE = pd.Timestamp("2026-09-30")  # 审计基准日

# ---------- 1. 读取明细 ----------
df = pd.read_excel("应收明细_假数据.xlsx")
df["发生日期"] = pd.to_datetime(df["发生日期"])
df["账龄天数"] = (BASE_DATE - df["发生日期"]).dt.days

# ---------- 2. 分账龄区间 ----------
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

# ---------- 3. 按客户 + 账龄区间 透视汇总 ----------
pivot = df.pivot_table(
    index="客户名称",
    columns="账龄区间",
    values="金额",
    aggfunc="sum",
    fill_value=0,
)

cols = ["0-30天", "31-60天", "61-90天", "90天以上"]
for c in cols:
    if c not in pivot.columns:
        pivot[c] = 0
pivot = pivot[cols]

# 加"合计"列
pivot["合计"] = pivot.sum(axis=1)

# 加"总计"行
pivot.loc["总计"] = pivot.sum()

print("=== 账龄分析表 ===")
print(pivot)

# ---------- 4. 坏账计提测算 ----------
rates = {
    "0-30天": 0.05,
    "31-60天": 0.10,
    "61-90天": 0.30,
    "90天以上": 0.50,
}

# 去掉"总计"行，只用各客户明细汇总
detail = pivot.drop("总计", errors="ignore")

provision = pd.DataFrame({"账龄区间": cols})
provision["金额"] = [round(detail[c].sum(), 2) for c in cols]
provision["计提比例"] = [f"{rates[c]*100:.0f}%" for c in cols]
provision["坏账准备"] = [round(detail[c].sum() * rates[c], 2) for c in cols]

# 先算应计提总额（仅各区间，不含合计行）
total_provision = round(provision["坏账准备"].sum(), 2)

# 再加"合计"行
provision.loc[len(provision)] = [
    "合计",
    round(provision["金额"].sum(), 2),
    "",
    round(provision["坏账准备"].sum(), 2),
]

print("\n=== 坏账计提测算 ===")
print(provision)
print(f"\n应计提坏账准备总额：{total_provision:,.2f}")

# ---------- 5. 输出 Excel（两个 sheet） ----------
with pd.ExcelWriter("8_账龄分析结果.xlsx") as writer:
    pivot.to_excel(writer, sheet_name="账龄分析")
    provision.to_excel(writer, sheet_name="坏账计提", index=False)

print("\n已生成：8_账龄分析结果.xlsx（含 sheet：账龄分析、坏账计提）")
