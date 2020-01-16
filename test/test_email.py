import emails
from emails.template import JinjaTemplate as T


USERNAME = 'mr_ranchou@163.com'
PASSWORD = 'ZX123456'
smtp_conf = {'host': 'smtp.163.com',
             'user': USERNAME,
             'password': PASSWORD}


def send_email():
    message = emails.html(subject=T('测试邮件'),
                          html=T('<p>详情见附件<br><br>'),
                          mail_from=('auto-reporter', USERNAME))
    message.attach(data=open('../log/2020-01-16 10-50-03.xlsx', 'rb'), filename="2020-01-16 10-50-03.xlsx")
    r = message.send(to=USERNAME, smtp=smtp_conf)
    print(r)


def office365():
    import smtplib
    mailserver = smtplib.SMTP('smtp.office365.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(USERNAME, PASSWORD)
    mailserver.sendmail(USERNAME, USERNAME, 'python email')
    mailserver.quit()


if __name__ == "__main__":
    send_email()
