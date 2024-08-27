#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import zmail as zmail

from config.conf import cm


def send_report():
    """发送报告"""
    with open(cm.REPORT_FILE, encoding='gbk') as f:
        content_html = f.read()
    try:
        mail = {
            'from': '',
            'subject': '最新的测试报告邮件',
            'content_html': content_html,
            'attachments': [cm.REPORT_FILE, ]
        }
        server = zmail.server(*cm.EMAIL_INFO.values())
        server.send_mail(cm.ADDRESSEE, mail)
        print("测试邮件发送成功！")
    except Exception as e:
        print("Error: 无法发送邮件，{}！", format(e))


if __name__ == "__main__":
    '''请先在config/conf.py文件设置QQ邮箱的账号和密码'''
    send_report()