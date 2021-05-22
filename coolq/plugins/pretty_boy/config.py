class CustomConfig(object):
    redis_host = "redis"
    redis_port = 3306
    db = 0  # 存储位置
    redis_expire = 86400  # 秒
    BLPOP_TIMEOUT = 10  # 取数超时时间
    pretty_boy_key = "pretty_boy:key"

    group_id = '97795387'
    bot_id = '732599980'
