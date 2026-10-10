# 2_make_report.py
# 生成假的审计报告 Word，内含一张资产负债表表格

from docx import Document

doc = Document()
doc.add_heading("审计报告（假数据）", level=1)
doc.add_paragraph("以下是模拟的资产负债表部分表格：")

# 表格数据：项目 / 期末余额
rows = [
    ("项目", "期末余额"),
    ("货币资金", 205000),
    ("应收账款", 80000),      # 故意写错，TB 正确是 75000
    ("存货", 60000),
    ("固定资产", 250000),
    ("资产总计", 590000),
    ("", ""),
    ("应付账款", 70000),
    ("实收资本", 400000),
    ("未分配利润", 120000),
    ("负债和所有者权益总计", 590000),
]

table = doc.add_table(rows=len(rows), cols=2)
table.style = "Table Grid"

for i, (a, b) in enumerate(rows):
    table.cell(i, 0).text = str(a)
    table.cell(i, 1).text = str(b)

doc.save("审计报告_假数据.docx")

print("已生成：审计报告_假数据.docx")