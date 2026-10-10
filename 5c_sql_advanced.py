# 5c_sql_advanced.py
# SQL 进阶：HAVING、ORDER BY、CASE

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

# 查询 4：HAVING——分组后筛选
查询("""
SELECT 科目名称, SUM(借方) AS 借方合计
FROM vouchers
GROUP BY 科目名称
HAVING SUM(借方) >= 10000
""", "借方合计 >= 10000 的科目")

# 查询 5：ORDER BY——排序
查询("""
SELECT 科目名称, SUM(借方) AS 借方合计
FROM vouchers
GROUP BY 科目名称
ORDER BY 借方合计 DESC
""", "按借方合计从大到小排")

# 查询 6：CASE——条件判断（相当于 Python 的 if）
查询("""
SELECT 凭证号, 科目名称, 借方, 贷方,
       CASE
           WHEN 借方 > 0 THEN '借'
           WHEN 贷方 > 0 THEN '贷'
           ELSE '无'
       END AS 方向
FROM vouchers
""", "给每行标注借贷方向")

conn.close()