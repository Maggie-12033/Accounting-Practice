# 6b_sql_practice.py
# SQL 实战：Top N + 期末余额

import sqlite3
import pandas as pd

conn = sqlite3.connect("practice.db")

def 查询(sql, 说明):
    print("=" * 60)
    print("【" + 说明 + "】")
    print("-" * 60)
    df = pd.read_sql(sql, conn)
    print(df)
    print()

# 实战 1：借方发生额前 3 的科目
查询("""
SELECT 科目名称,
       SUM(借方) AS 借方合计
FROM vouchers
GROUP BY 科目名称
HAVING SUM(借方) > 0
ORDER BY 借方合计 DESC
LIMIT 3
""", "借方发生额前 3 的科目")

# 实战 2：每个科目的期末余额（借方合计 - 贷方合计）
查询("""
SELECT a.科目类别,
       v.科目代码,
       a.科目名称,
       SUM(v.借方) - SUM(v.贷方) AS 期末余额
FROM vouchers AS v
JOIN accounts AS a ON v.科目代码 = a.科目代码
GROUP BY a.科目类别, v.科目代码, a.科目名称
ORDER BY a.科目类别, v.科目代码
""", "各科目期末余额（借-贷）")

conn.close()