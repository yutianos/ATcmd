#!/usr/bin/env python3.5

#  Author: Eric
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

mailserver = "smtp.126.com"
user = 'yutianos@126.com'
passwd = 'root123'
from_addr = "yutianos@126.com"
to_addr = "2216015598@qq.com"
sendmsg = "我爱你"

def mail():
    
    ret = True
    try:
        msg = MIMEText(sendmsg, 'plain', 'utf-8')
        msg['From'] = formataddr(["Raspiberry", "yutianos@126.com"])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", "2216015598@qq.com"])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "MESSAGE From Raspiberry"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.126.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(user, passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(user, [to_addr, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接

    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret
        
ret = mail()
if ret:
    pass
else:
    pass
