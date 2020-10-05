# 自定义过滤器

# 数字格式化过滤器
def number_split(num):
    """数字格式化 12345678 = 12，345，678
        :param num :需要格式化的数据
        :return:格式化后的字符串
    """
    return '{:,}'.format(int(num))