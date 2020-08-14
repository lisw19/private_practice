import hashlib
import random
import string


def verify(value, rc, key='duplicate_default', skip=False):
    """
    验证是否存在去重集合中
    :param value: 去重值
    :param rc: redis连接
    :param key: redis key
    :param dont_filter: 是否跳过过滤
    :return:
    """
    if skip:
        return False
    if '.aspx' in str(value) and '(' in str(value):
        value = str(value).split('(')[0] + str(value).split(')')[
            len(str(value).split(')')) - 1]
    if not key:
        return False
    if rc.sismember(key, value):
        return True
    return False


def confirm(value, rc, key='duplicate_default', skip=False):
    """
    把值加入去重集合中
    :param value: 去重值
    :param rc: redis连接
    :param key: redis key
    :return:
    """
    if not skip:
        rc.sadd(key, value)
        rc.expire(key, 3600 * 24 * 7)


def task_filter(value, rc, key='duplicate_default', skip=False):
    """
    任务去重
    :param value:
    :param rc:
    :param key:
    :param skip:
    :return:
    """
    if skip:
        return False
    if not rc.sismember(key, value):
        rc.sadd(key, value)
        rc.expire(key, 3600 * 24 * 7)
        return False
    return True


def unique_uid(*args, **kwargs):
    """
    generator only uid
    生成唯一识别符(传入的值是可变参数)
    """
    str_tmp = ''
    if args:
        str_tmp = ''.join('%s' % i for i in args)
    if kwargs:
        str_tmp = ''.join('%s' % b for a, b in kwargs.items())
    md5_str = hashlib.md5(str_tmp.encode()).hexdigest()
    return md5_str


def random_string(digit=64):
    """
    生成固定位数的随机组合
    params: digit: <int> 位数
    """
    src_digits = string.digits
    src_uppercase = string.ascii_uppercase
    src_lowercase = string.ascii_lowercase
    src_total = src_digits + src_uppercase + src_lowercase

    # 生成字符串
    random_first = digit // 3
    random_two = digit - random_first - 1
    random_three = digit - random_first - random_two

    digits_num = random.sample(src_total, random_first)
    uppercase_num = random.sample(src_total, random_two)
    lowercase_num = random.sample(src_total, random_three)
    _string = digits_num + uppercase_num + lowercase_num
    random.shuffle(_string)
    target_string = ''.join(_string)
    return target_string


if __name__ == '__main__':
    print(unique_uid('fsdnfakdfn'))
    # print(unique_uid(u'fsdnfakdfn'))
    # print(unique_uid(['fsdnfakdfn']))
    # print(unique_uid({
    #     'name': 'spiders',
    #     'age': '18'
    # }))
    # test_dict = {
    #     'name': 'spiders',
    #     'age': '18'
    # }
    # print(unique_uid(**test_dict))
    # print(random_string())
    # print(random_string(32)
