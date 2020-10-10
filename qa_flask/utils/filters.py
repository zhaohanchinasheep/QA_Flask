# 自定义过滤器

# 数字格式化过滤器
from datetime import datetime

import timeago


def number_split(num):
    """数字格式化 12345678 = 12，345，678
        :param num :需要格式化的数据
        :return:格式化后的字符串
    """
    return '{:,}'.format(int(num))

def dt_format_show(dt):
    """
    日期和时间，格式化显示
    3分钟前
    2小时前
    :param dt:datetime 时间
    :return:格式化后的时间
    """
    now = datetime.now()
    # 返回：now到dt的间隔时间
    return timeago.format(dt,now,'zh_CN')