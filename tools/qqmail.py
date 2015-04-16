# -*-coding:utf-8-*-
# Author: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import smtplib
from email.mime.text import MIMEText

class QQMail(object):
    def __init__ (self ,account, password):
        self.account="%s@qq.com" %account
        self.password=password

    def send (self, to_list, title, content):
        # print self.account,self.password
        server = smtplib.SMTP('smtp.qq.com')
        server.set_debuglevel(1)
        ## server.docmd("EHLO server" )
        ## server.starttls()
        server.login(self.account, self.password)

        for addr in to_list:
            msg = MIMEText(content)
            msg['Content-Type' ]='text/plain; charset="utf-8"'
            msg['Subject' ] = title
            msg['From' ] = self.account
            msg['To' ] = addr
            server.sendmail(self.account, addr, msg.as_string())
        server.close()


if __name__ == '__main__':
    qqmail = QQMail("584544233","dslwz020415")
    qqmail.send(["67070868@qq.com","dslwz2002@163.com"], "test mail", "this is a test mail from a friend.")