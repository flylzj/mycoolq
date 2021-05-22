import redis

from coolq.plugins.pretty_boy.config import CustomConfig


class Redis(object):
    """
    redis数据库操作
    """

    @staticmethod
    def _get_r():
        r = redis.StrictRedis(host=CustomConfig.redis_host,
                              port=CustomConfig.redis_port,
                              db=CustomConfig.db)
        return r

    @staticmethod
    def get_r(host, port, db):
        r = redis.StrictRedis(host=host,
                              port=port,
                              db=db)
        return r

    @classmethod
    def expire(cls, name, expire=None):
        """
        设置过期时间
        :param name:
        :param expire:
        :return:
        """
        expire_in_seconds = expire if expire else CustomConfig.redis_expire
        r = cls._get_r()
        r.expire(name, expire_in_seconds)

    @classmethod
    def write(cls, key, value, expire=None):
        expire_in_seconds = expire if expire else CustomConfig.redis_expire
        r = cls._get_r()
        r.set(key, value, ex=expire_in_seconds)

    @classmethod
    def read(cls, key):
        r = cls._get_r()
        value = r.get(key)
        return value.decode('utf-8') if value else value

    @classmethod
    def hset(cls, name, key, value):
        r = cls._get_r()
        r.hset(name, key, value)

    @classmethod
    def hget(cls, name, key):
        r = cls._get_r()
        if name is None:
            return None
        value = r.hget(name, key)
        return value.decode('utf-8') if value else value

    @classmethod
    def hgetall(cls, name):
        r = cls._get_r()
        return r.hgetall(name)

    @classmethod
    def delete(cls, names):
        """
        :param names: 一个或者多个
        :return:
        """
        r = cls._get_r()
        r.delete(names)

    @classmethod
    def lpush(cls, name, values):
        """
        :param values: 一个或者多个: 如果是可迭代对象 记得解包
        :param name:
        :return:
        """
        r = cls._get_r()
        r.lpush(name, values)

    @classmethod
    def blpop(cls, key, timeout=10):
        """
        :param timeout: 如果是0则可能会无限阻塞
        :param key
        :return:
        """
        if timeout <= 0:
            timeout = CustomConfig.BLPOP_TIMEOUT
        if key is None:
            return None
        r = cls._get_r()
        value = r.blpop(key, timeout=timeout)
        if isinstance(value, (tuple, list)):
            value = [i.decode('utf-8') for i in value]
        else:
            value.decode('utf-8') if value else value
        return value

    @classmethod
    def llen(cls, name):
        """
        获取key的长度
        :param name:
        :return:
        """
        if name is None:
            return 0
        r = cls._get_r()
        return r.llen(name)

