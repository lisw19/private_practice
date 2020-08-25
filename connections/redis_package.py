import redis

from tools.time_package import change_to_timestamp


class MyRedis(object):
    """
    redis连接
    """

    def __init__(self, **kwargs):
        config = {'host': '127.0.0.1',
                  'port': 6379, 'db': 0}
        if kwargs:
            config.update(kwargs)
        self.pool = redis.ConnectionPool(decode_responses=True, **config)
        try:
            self.conn = redis.StrictRedis(connection_pool=self.pool)
            self.pipe = self.conn.pipeline()
        except Exception as E:
            print('[REDIS][CONN FAIL]info:{}'.format(repr(E)))

    def execute_command(self, *args, **kwargs):
        return self.conn.execute_command(*args, **kwargs)

    def close(self):
        self.pool.disconnect()
        print('[REDIS][CONN CLOSED]')

    def __del__(self):
        try:
            self.pool.disconnect()
        except Exception:
            pass

    def batch_del_key(self, key_prefix):
        """
        删除指定key前缀的所有key
        :param:key_prefix<str>: 指定key前缀
        """
        keys_set = iter(self.execute_command('KEYS', '%s*' % key_prefix))
        for sin_key in keys_set:
            self.execute_command('DEL', sin_key)
        return True


class MyCache(MyRedis):
    """
    基础缓存模块
    """

    def __init__(self, **kwargs):
        config = {}
        if kwargs:
            config['host'] = kwargs.get('host')
            config['port'] = kwargs.get('port')
            config['password'] = kwargs.get('pwd') if kwargs.get('pwd') else kwargs.get('password')
            config['db'] = kwargs.get('db', 0)
        super().__init__(**config)
        self._log = '[CACHE MODEL]'

    def show_caches(self, rc='*', size=200):
        """
        罗列已有的定时缓存
        {'name': key, 'life': life}
        name为具体的缓存key，life为具体的key所剩余的缓存时间
        :param: rc：<re>支持正则
        :param: size：<int> 拿出key数量 默认200
        :return:
        """
        res = []
        keys = list(self.conn.scan_iter(rc, count=size))
        if not keys:
            print(self._log + f'cmd:({rc}) no cache')
            return res
        res = [{'name': key, "life": self.execute_command('ttl', key)} for key in keys]
        return res

    def create_cache(self, cache_name, expires, cache_type=True):
        """
        新建定时缓存
        :param cache_name: 缓存key
        :param expires: <int/date> 建立缓存的有效期,可整数也可日期字符串
        :param cache_type: <bool>缓存类型，如果True: 为set类型，False:string类型
        :return <bool>: 所建缓存已存在返回False;不存在且新建缓存失败返回False; 不存在返回True,并新建缓存
        """
        all_keys = self.show_caches(rc=cache_name)
        for key in all_keys:
            name = key.get('name')
            life = key.get('life')
            if name == cache_name and life != -1:
                print(self._log + '[CACHE EXISTS]cache_name:({}) existed'.format(cache_name))
                return False
        self.delete(cache_name)
        if cache_type:
            self.conn.sadd(cache_name, cache_name)
        else:
            self.conn.set(cache_name, '1')

        # 增加缓存过期时间
        res_state = False
        if isinstance(expires, int):
            self.conn.expire(cache_name, expires)
            res_state = True
        elif isinstance(expires, str):
            if ':' in expires:
                expires = change_to_timestamp(expires, '%Y-%m-%d %H:%M:%S')
            else:
                expires = change_to_timestamp(expires, '%Y-%m-%d')
            self.conn.expireat(cache_name, expires)
            res_state = True
        if not res_state:
            self.delete(cache_name)
        print(self._log + f'[CREATE CACHE]key:{cache_name}, ex: {expires}')
        return res_state

    def add(self, cache_name, *args):
        """
        向指定集合缓存中填充元素
        :param cache_name:
        :param args:
        :return:
        """
        if not self.conn.exists(cache_name):
            print(self._log + '[add]cache_name non-existent.')
            return
        add_res = self.conn.sadd(cache_name, *args)
        return add_res

    def is_contain(self, cache_name, value):
        """
        判断元素是否在该集合缓存内
        :param cache_name:
        :param value:
        :return:
        """
        if not self.conn.exists(cache_name):
            print(self._log + '[is_contain]cache_name non-existent.')
            return
        is_in = self.conn.sismember(cache_name, value)
        return is_in

    def delete(self, cache_name, *args):
        """
        删除某集合缓存
        :param cache_name:3
        :param args:
        :return:
        """
        res_cache_name = [] + list(args)
        if isinstance(cache_name, str or int):
            res_cache_name.append(cache_name)
        if isinstance(cache_name, list):
            res_cache_name += cache_name
        for name in res_cache_name:
            self.conn.delete(name)
        return True


if __name__ == '__main__':
    a = MyCache()
    # a.create_cache('cde_clinical_trial_typeid_20', '2020-10-23')
    print(a.execute_command('KEYS', '*'))

    a.close()
