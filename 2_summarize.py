# 2_summarize.py
# 读取凭证表，按科目汇总借贷发生额，输出汇总表

import pandas as pd

df = pd.read_excel("凭证表_假数据.xlsx")

print("读入成功，共", len(df), "行")
print("列名：", list(df.columns))

summary = df.groupby(["科目代码", "科目名称"], as_index=False).agg({
    "借方金额": "sum",
    "贷方金额": "sum",
})

summary["净额"] = summary["借方金额"] - summary["贷方金额"]
summary = summary.sort_values("科目代码")

summary.to_excel("科目汇总表.xlsx", index=False)

print("\n汇总完成，已生成：科目汇总表.xlsx")
print(summary)