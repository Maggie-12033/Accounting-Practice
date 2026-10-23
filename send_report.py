# send_report.py
# 自动发送带 Excel 附件的邮件

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import os

import os
from dotenv import load_dotenv

# 1. 加载 .env 文件里的秘密
load_dotenv()

发件邮箱 = os.getenv("发件邮箱")
授权码 = os.getenv("授权码")
收件邮箱 = os.getenv("收件邮箱")
附件路径 = "账龄分析表.xlsx"  # 这个不涉密，可以直接写

# 构造带附件的邮件
msg = MIMEMultipart()
msg["Subject"] = Header("【自动报表】应收账款账龄分析结果", "utf-8")
msg["From"] = 发件邮箱
msg["To"] = 收件邮箱

# 1. 邮件正文
body = """
领导您好：

这是系统自动生成的应收账款账龄分析底稿，请查收附件。

（本邮件由 Python 脚本自动发送）
"""
msg.attach(MIMEText(body, "plain", "utf-8"))

# 2. 添加 Excel 附件
try:
    with open(附件路径, "rb") as f:
        part = MIMEApplication(f.read())
        # 把附件命名
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(附件路径))
        msg.attach(part)
except FileNotFoundError:
    print(f"找不到附件：{附件路径}，请检查路径。")
    exit()

# 3. 发送邮件
smtp_server = "smtp.qq.com"
smtp_port = 465

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(发件邮箱, 授权码)
    server.sendmail(发件邮箱, [收件邮箱], msg.as_string())
    server.quit()
    print("带附件的邮件发送成功！")
except Exception as e:
    print(f"发送失败：{e}")