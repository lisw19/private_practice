import time
import datetime
import functools


def date_time(offset_day=0, special_date=False, time_type='str'):
    """
    :param offset_day: <int> Days in advance
    :param special_date:<str>  String day，若给定，则在此基础上推移
    :param time_type:<str>  str 返回str类型时间；
                            dt 返回datetime.datetime；
    :return:
    :example:
      date_time()
      date_time(1)
      date_time(1, special_date='2019-01-02')
      date_time(1, special_date='2019-01-02 00:00:00')
    """

    def _change_time_type(time_element, ft='%Y-%m-%d'):
        """
        切换时间格式
        :param time_element:
        :param ft:
        :return:
        """
        _res_date = time_element.strftime(ft)
        if time_type == 'dt':
            _res_date = time_element
        return _res_date

    assert time_type in ('str', 'dt'), TypeError('time type dont supported, exp:"str"or"dt"')
    today = datetime.date.today()
    fmt = '%Y-%m-%d'
    if special_date:
        assert isinstance(special_date, str), TypeError('time_type type error!')
        if len(special_date) > 10:
            fmt = '%Y-%m-%d %H:%M:%S'
        today = datetime.datetime.strptime(special_date, fmt)
    offday = datetime.timedelta(offset_day)
    target_day = today - offday
    return _change_time_type(target_day, fmt)


def current_time(time_format='%Y-%m-%d %H:%M:%S'):
    """
    返回格式化后的当前时间
    """
    current_time = str(datetime.datetime.now().strftime(time_format))
    return current_time


def get_first_day_of_month(return_type: str = 'int',
                           ts: int = 0,
                           return_foramt='%Y-%m-%d %H:%M:%S'):
    """
    获取本月第一天
    :param ts:
    :param return_type: <str> int默认返回时间戳/str 返回日期
    :return
    """
    if ts:
        day = datetime.datetime.fromtimestamp(ts)
    else:
        day = datetime.date.today()
    day_of_month = day - datetime.timedelta(days=day.day - 1)
    dt = datetime.datetime(day_of_month.year, day_of_month.month, day_of_month.day, 0, 0, 0)
    t = dt.timetuple()
    time_stamp = int(time.mktime(t))
    res = time_stamp
    if return_type == 'str':
        time_array = time.localtime(time_stamp)
        res = time.strftime(return_foramt, time_array)
    return res


def get_time_delta(time_type='hours', time_delta=1.0, is_all=False):
    """
    获取时间差，支持小时/天/分钟/秒
    :param: time_type: 时间类型 day/hour/minute/second
    :param: time_delta: 时间间隔（按照小时/单位）
    :param: is_all<bool> 是否拼接字段
    """
    current_time = datetime.datetime.now()
    if time_type == 'days':
        _time_res = current_time - datetime.timedelta(days=time_delta / 24)
        time_res = _time_res.strftime("%Y-%m-%d")
    elif time_type == 'hours':
        _time_res = current_time - datetime.timedelta(hours=time_delta)
        time_res = _time_res.strftime("%Y-%m-%d %H")
    elif time_type == 'minutes':
        _time_res = current_time - datetime.timedelta(minutes=time_delta * 60)
        time_res = _time_res.strftime("%Y-%m-%d %H:%M")
    elif time_type == 'seconds':
        _time_res = current_time - datetime.timedelta(seconds=time_delta * 60 * 60)
        time_res = _time_res.strftime("%Y-%m-%d %H:%M:%S")
    else:
        raise TypeError('time_type type error!')
    if is_all:
        time_res = _time_res.strftime("%Y-%m-%d %H:%M:%S")
    return time_res


def change_to_timestamp(str_time, ft='%Y-%m-%d'):
    """
    str时间转timestamp
    :param str_time: <str> strtime
    :param ft: 格式
    :return:
    """
    time_array = time.strptime(str_time, ft)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def get_current_timestamp(is_second_or_millisecond=True):
    """
    获取当前时间戳
    :params: is_second_or_millisecond: <bool>
    :return: current timestamp
    """
    if is_second_or_millisecond:
        current_timestamp = int(time.time())
    else:
        current_timestamp = int(round(time.time() * 1000))
    return current_timestamp


def time_section(type='year', return_type='int'):
    """
    time section dealer
    input:year output:2018
    input:month output:05/5
    input:second output:05/5
    :param type: <str> year/month/day/hour/minute/second/week
    :param return_type: <str> final result type is int or str, 默认返回 int
    :return:
    """
    if type == 'year':
        target = datetime.datetime.now().date().year
    elif type == 'month':
        target = datetime.datetime.now().date().month
    elif type == 'day':
        target = datetime.datetime.now().date().day
    elif type == 'week':
        target = datetime.datetime.now().weekday() + 1
    elif type == 'hour':
        target = datetime.datetime.now().hour
    elif type == 'minute':
        target = datetime.datetime.now().minute
    elif type == 'second':
        target = datetime.datetime.now().second
    else:
        raise Exception('type error')
    if return_type == 'str':
        return str(target)
    return target


def get_week_today(ts=None):
    """
    获得今天是周几0-6对应周日到周六
    """
    a = time.localtime()
    if ts:
        a = time.localtime(ts)
    return int(time.strftime('%w', a))


def format_str_date(pend_date, reverse=False):
    """
    字符串时间 和 时间格式相互转换
    :param pend_date:<str>shijian
    :param reverse:<bool> 默认false即字符串时间转时间格式，
                              ture即时间格式转str
    :return:
    """
    assert pend_date and isinstance(pend_date, (str, datetime.datetime, datetime.date)), \
        TypeError('time_type type error!')
    ft = '%Y-%m-%d %H:%M:%S'
    if len(str(pend_date)) < 11:
        ft = '%Y-%m-%d'
    if isinstance(pend_date, (datetime.datetime, datetime.date)):
        if not reverse:
            return pend_date
        return pend_date.strftime(ft)
    # 2020-06-09 20:55:59.145
    str_date_time = pend_date.split('.')[0]
    res_date_time = datetime.datetime.strptime(str_date_time, ft)
    return res_date_time


def get_date_list(start, end, fmt="%Y-%m-%d %H:%M:%S", is_reverse=False):
    """
    获取日期区间列表
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    start = format_str_date(start)
    end = format_str_date(end)
    data = []
    day = datetime.timedelta(days=1)
    for i in range((end - start).days):
        re = start + day * i
        data.append(re.strftime(fmt))
    data.append(end.strftime(fmt))
    if is_reverse:
        data.reverse()
    return data


def check_func_time(func):
    """
    判断函数运行时间
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = get_current_timestamp(is_second_or_millisecond=False)
        func_state = func(*args, **kwargs)
        end_time = get_current_timestamp(is_second_or_millisecond=False)
        delta_time = int(end_time - start_time) / 1000
        print('%s use %ss' % (func.__name__, delta_time))
        return func_state

    return wrapper


if __name__ == '__main__':
    # print(change_to_timestamp())
    # print(current_time())
    # print(current_time(time_format='%Y-%m-%d'))
    # print(get_time_delta())
    # print(6 - get_week_today())
    # print(get_date_list('2019-1-1 10:00:00', '2019-10-1', fmt='%d/%m/%Y'))
    # a = change_to_timestamp(date_time(-1), ft='%Y-%m-%d')
    # print(a)
    print(get_first_day_of_month(return_type='str'))
    # print(get_time_delta(time_type='hours', time_delta=1, is_all=True))
    # print(date_time(1, special_date='2019-01-02 00:00:00'))
    # print(get_current_timestamp())
    # print(get_current_timestamp(is_second_or_millisecond=False))
    # print(time_section('day'))
    # print(time_section('hour'))
    # print(current_time())
    # print(current_time('%Y-%m-%d %H:%M'))
    # print(get_time_delta(time_type='days', time_delta=45))
    # print(get_time_delta(time_type='hours', time_delta=2))
    # print(get_time_delta(time_type='minutes', time_delta=1/6))
    # print(get_time_delta(time_type='seconds', time_delta=1))
    # print(get_time_delta(time_type='hours', time_delta=1, is_all=True))
    # print(get_time_delta(time_type='minutes', time_delta=1, is_all=True))
