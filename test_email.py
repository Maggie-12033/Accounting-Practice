# test_email.py
# 测试发邮件

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# ===== 配置区（改成你自己的）=====
发件邮箱 = "2265476840@qq.com"
授权码 = "sxgwjsosswsjdjbg"
收件邮箱 = "2265476840@qq.com"   # 先发给自己测试
# ==================================

# 构造邮件
msg = MIMEText("这是一封 Python 自动发送的测试邮件。", "plain", "utf-8")
msg["Subject"] = Header("测试邮件", "utf-8")
msg["From"] = 发件邮箱
msg["To"] = 收件邮箱

# 连接 QQ 邮箱 SMTP 服务器
smtp_server = "smtp.qq.com"
smtp_port = 465   # SSL 加密端口

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(发件邮箱, 授权码)
    server.sendmail(发件邮箱, [收件邮箱], msg.as_string())
    server.quit()
    print("发送成功！去邮箱看看。")
except Exception as e:
    print(f"发送失败：{e}")