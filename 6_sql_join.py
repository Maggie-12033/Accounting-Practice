# 6_sql_join.py
# SQL 多表关联（JOIN）

import sqlite3
import pandas as pd

conn = sqlite3.connect("practice.db")
cursor = conn.cursor()

# 建"科目表"
cursor.execute("DROP TABLE IF EXISTS accounts")
cursor.execute("""
CREATE TABLE accounts (
    科目代码 TEXT,
    科目名称 TEXT,
    科目类别 TEXT
)
""")

accounts_data = [
    ("1001", "库存现金",     "资产"),
    ("1002", "银行存款",     "资产"),
    ("1122", "应收账款",     "资产"),
    ("1405", "库存商品",     "资产"),
    ("2202", "应付账款",     "负债"),
    ("4001", "实收资本",     "权益"),
    ("6001", "主营业务收入", "损益"),
    ("6401", "主营业务成本", "损益"),
    ("6602", "管理费用",     "损益"),
]
cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?)", accounts_data)
conn.commit()

def 查询(sql, 说明):
    print("=" * 60)
    print("【" + 说明 + "】")
    print("-" * 60)
    df = pd.read_sql(sql, conn)
    print(df)
    print()

# 查询 7：JOIN——凭证表和科目表关联
查询("""
SELECT v.凭证号, v.科目代码, a.科目名称, a.科目类别, v.借方, v.贷方
FROM vouchers AS v
JOIN accounts AS a ON v.科目代码 = a.科目代码
""", "凭证 + 科目类别（关联后）")

# 查询 8：JOIN + GROUP BY——按科目类别汇总
查询("""
SELECT a.科目类别,
       SUM(v.借方) AS 借方合计,
       SUM(v.贷方) AS 贷方合计
FROM vouchers AS v
JOIN accounts AS a ON v.科目代码 = a.科目代码
GROUP BY a.科目类别
""", "按科目类别汇总借贷")

conn.close()