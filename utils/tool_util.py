import random

from datetime import datetime


def random_number(num):
    str = ""
    for i in range(num):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    return str


# 比较俩个时间的差异
def time_lag(time, times):
    d1 = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(times, '%Y-%m-%d %H:%M:%S')
    delta = d1 - d2
    return delta


# 原料牌号返回
def goods_mark(num):
    # 选择 原料牌号
    yl_mark = "div.ant-modal-body div:nth-child(" + str(num) + ")"
    return yl_mark


def goods_deliver_area(area):
    deliver_area = "xpath==//*[contains(text()," + area + ")]"
    return deliver_area


def unicode_name():
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)


def gbk2312_name():
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xfe)
    val = f'{head:x} {body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str


def look_for_text(loc):
    xpath = "//*[contains(text()," + loc + ")]"
    return xpath

