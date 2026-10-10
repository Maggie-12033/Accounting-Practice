# 3_check.py
# 核对 TB 与审计报告（Word 表格）是否一致

import pandas as pd
from docx import Document

# ---------- 1. 读 TB ----------
tb = pd.read_excel("TB_假数据.xlsx")
tb["净额"] = tb["期末借方"].fillna(0) - tb["期末贷方"].fillna(0)
tb["科目代码"] = tb["科目代码"].astype(str)
tb_map = dict(zip(tb["科目代码"], tb["净额"]))

# ---------- 2. 按规则合成报表项目 ----------
# 格式：报表项目: [(科目代码, 方向), ...]
# 方向 1 = 加，-1 = 减（备抵科目、贷方余额科目用 -1）
rules = {
    "货币资金":   [("1001", 1), ("1002", 1)],
    "应收账款":   [("1122", 1), ("1231", 1)],    # 改：坏账准备已是负数，直接加
    "存货":       [("1405", 1)],
    "固定资产":   [("1601", 1), ("1602", 1)],    # 改：累计折旧已是负数，直接加
    "应付账款":   [("2202", -1)],
    "实收资本":   [("4001", -1)],
    "未分配利润": [("4103", -1)],
}


tb_report = {}
for item, parts in rules.items():
    total = sum(tb_map.get(code, 0) * sign for code, sign in parts)
    tb_report[item] = total
    print("调试：", item, parts, "=>", total)

# ---------- 3. 读 Word 报告表格 ----------
doc = Document("审计报告_假数据.docx")
table = doc.tables[0]

report_data = {}
for row in table.rows:
    item = row.cells[0].text.strip()
    amount = row.cells[1].text.strip()
    if item and amount:
        try:
            report_data[item] = float(amount)
        except ValueError:
            pass

# ---------- 4. 对比 ----------
print("=== 核对结果 ===")
print(f"{'项目':<12}{'TB算出':>12}{'报告数':>12}{'差异':>12}")
print("-" * 52)

for item in rules.keys():
    tb_val = tb_report[item]
    rpt_val = report_data.get(item)
    if rpt_val is None:
        print(f"{item:<12}{tb_val:>12.2f}{'（报告缺此项）':>12}")
        continue
    diff = tb_val - rpt_val
    flag = "  ← 不一致" if abs(diff) > 0.01 else ""
    print(f"{item:<12}{tb_val:>12.2f}{rpt_val:>12.2f}{diff:>12.2f}{flag}")