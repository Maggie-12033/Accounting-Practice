# merge_excel.py
# 批量合并同一个文件夹下所有的 Excel 文件

import pandas as pd
import os
import glob

# 1. 设定文件夹路径
folder_path = "monthly_reports"

# 2. 找出文件夹下所有的 xlsx 文件
# glob 会帮我们找出所有符合规则的文件
file_list = glob.glob(os.path.join(folder_path, "*.xlsx"))

print(f"找到了 {len(file_list)} 个 Excel 文件，开始合并...")

# 3. 循环读取并存入列表
all_data = []
for file in file_list:
    # 读取每个文件
    df = pd.read_excel(file)
    # 为了让数据不乱，我们可以新增一列，记下这行数据来自哪个文件
    df["来源文件"] = os.path.basename(file) 
    all_data.append(df)

# 4. 把列表里的所有表格拼成一个大表
# ignore_index=True 表示重新排一下行号
final_df = pd.concat(all_data, ignore_index=True)

# 5. 输出结果
output_file = "全年合并总表.xlsx"
final_df.to_excel(output_file, index=False)

print(f"合并完成！总共 {len(final_df)} 行数据。")
print(f"已生成：{output_file}")