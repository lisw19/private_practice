import sys
import time
import json
import random
import requests
import functools

from copy import deepcopy
from inspect import signature
from concurrent.futures.thread import ThreadPoolExecutor


class Check(object):
    """
    适用于各种情景检查功能
    """

    @staticmethod
    def pos_html(h, pos=None):
        """
        检查是否h中是否包含pos
        :params: h: 下载后的html
        :params: pos: 是否包含
        :return: <bool> true/false
        """
        if Check.is_json(h):
            return True
        if not pos:
            pos = ['<html>']
        for i in pos:
            if str(i).strip() in h:
                return True
        return False

    @staticmethod
    def is_json(my_json):
        """
        判断是否是json类型
        """
        try:
            json.loads(my_json)
        except ValueError:
            return False
        return True

    @staticmethod
    def is_dict_value_null(target_dict, pop_keys=None):
        """
        判断target_dict是否均为空
        False: 字典值中有数据
        True: 字典值中无数据
        :params: target_dict: <dict> 目标待处理字典
        :params: pop_keys: <list/str> 需要排除处理的key
        """
        __target_dict = deepcopy(target_dict)
        pop_keys_list = list()
        if isinstance(pop_keys, str):
            pop_keys_list.append(pop_keys)
        elif isinstance(pop_keys, list):
            pop_keys_list = pop_keys
        if pop_keys_list:
            for i in pop_keys_list:
                __target_dict.pop(i, '')
        for sin_va in __target_dict.values():
            if sin_va:
                return False
        return True

    @staticmethod
    def is_request_valid(url, timeout=30):
        """
        检测url是否可以请求通
        """
        try:
            res = requests.get(url, timeout=timeout)
        except requests.exceptions.ConnectTimeout:
            print('[IS_REQUEST_VALID]url:%s error: timeout' % url)
            return False
        except Exception as err:
            print('[IS_REQUEST_VALID]url:%s error:%s' % (url, err))
            return False
        res_status = res.status_code
        if res_status == 200:
            return True
        return False

    @staticmethod
    def is_compress_dict(target_dict):
        """
        是否将正常字典压缩（将字典中为空的值去除掉）
        """
        assert isinstance(target_dict, dict), 'param must be dict!'
        new_dict = dict()
        for sin_k, sin_v in target_dict.items():
            if not sin_v:
                continue
            new_dict[sin_k] = sin_v
        return new_dict

    @staticmethod
    def is_contains_chinese(strs):
        """
        检验字符串中是否含有中文字符
        """
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    @staticmethod
    def is_df_contains_value(df, column_name,
                             value, is_judge_origin=False):
        """
        检查df中的column_name列中是否包含value
        :param df: dataFrame
        :param column_name: df中的某列名
        :param value: <str> 某字符串（用来判断是否在df中）
        :param is_judge_origin: <bool> 是否需要判断初始df(和业务相关)
                  is_judge_origin:True 且初始df为空，则判定存在
        :return <bool> True:存在 False: 不存在
        """
        if is_judge_origin and df.empty:
            return True
        if column_name not in df.columns:
            raise TypeError('column_name not in df!')
        df_res = df.loc[df[column_name] == value]
        if df_res.empty:
            return False
        return True


class Bunch(dict):
    """
    Container object for datasets
    Dictionary-like object that exposes its keys as attributes.

    >>> b = Bunch(a=1, b=2)
    >>> b['b']
    2
    >>> b.b
    2
    >>> b.a = 3
    >>> b['a']
    3
    >>> b.c = 6
    >>> b['c']
    6
    """

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __dir__(self):
        return self.keys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)


def check_fun_error(func):
    """
    检查函数的报错
    如果函数自身报错，则重新运行函数本身
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            fun_res = func(*args, **kwargs)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            print('[ERROR] check_fun restart!, error info:%s, value:%s' % (
                exc_type, exc_value))
            time.sleep(random.uniform(2, 5))
            fun_res = func(*args, **kwargs)
        return fun_res

    return wrapper


def check_fun_return(func):
    """
    检查函数值是否报错更新返回值
    如果函数自身报错，则返回False,否则正常返回
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            fun_res = func(*args, **kwargs)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            print('check_fun return False!, error info:%s, value:%s' % (
                exc_type, exc_value))
            fun_res = False
        return fun_res

    return wrapper


def param_type_assert(*args, **kargs):
    """
    函数参数验证器
    :param args:
    :param kargs:
    :return:
    case:
    # @param_type_assert(d=int)
    # @param_type_assert(int, str)
    @param_type_assert(c=list, a=int)
    def demo(a, b, c, d=1):
        print(a, b, c, d)
    """

    def decorator(func):
        assert_func = signature(func)
        assert_param_dict = assert_func.bind_partial(*args, **kargs).arguments

        @functools.wraps(func)
        def wrapper(*args, **kargs):
            for param_name, param_value in assert_func.bind(*args, **kargs).arguments.items():
                if param_name in assert_param_dict:
                    if not isinstance(param_value, assert_param_dict[param_name]):
                        raise TypeError('[CHECK_PARAM] %s must be %s' % (param_name, assert_param_dict[param_name]))
            return func(*args, **kargs)

        return wrapper

    return decorator


MAX_THREAD_WORKER = 8
ECECUTER = ThreadPoolExecutor(max_workers=MAX_THREAD_WORKER)


def thread_pool(*, callbacks=(), callback_kwargs=()):
    """
    多线程装饰
    :param callbacks:
    :param callback_kwargs:
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            futuer = ECECUTER.submit(func, *args, **kwargs)
            for index, callback in enumerate(callbacks):
                try:
                    kwargs = callback_kwargs[index]
                except IndexError as E:
                    print(f"[THREAD_POOL]{repr(E)}")
                    kwargs = None
                fn = functools.partial(callback, **kwargs) if kwargs else callback
                futuer.add_done_callback(fn)
            return futuer

        return wrapper

    return decorator


if __name__ == '__main__':
    # @param_type_assert(d=int)
    # @param_type_assert(int, str)
    @param_type_assert(c=list, a=int)
    def demo(a, b, c, d=1):
        print(a, b, c, d)


    demo(1, '2', [1, 2])
