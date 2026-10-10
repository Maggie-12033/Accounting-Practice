# 5b_sql_queries.py
# SQL 查询练习

import sqlite3
import pandas as pd

conn = sqlite3.connect("practice.db")

def 查询(sql, 说明):
    print("=" * 60)
    print("【" + 说明 + "】")
    print(sql.strip())
    print("-" * 60)
    df = pd.read_sql(sql, conn)
    print(df)
    print()

# 查询 1：查全部
查询("""
SELECT * FROM vouchers
""", "查全部凭证")

# 查询 2：只看借方大于 5000 的
查询("""
SELECT 凭证号, 科目名称, 借方
FROM vouchers
WHERE 借方 > 5000
""", "借方大于 5000 的")

# 查询 3：按科目汇总借贷
查询("""
SELECT 科目代码, 科目名称,
       SUM(借方) AS 借方合计,
       SUM(贷方) AS 贷方合计
FROM vouchers
GROUP BY 科目代码, 科目名称
""", "按科目汇总")

conn.close()