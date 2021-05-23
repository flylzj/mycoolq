class CustomConfig(object):
    redis_host = "127.0.0.1"  # 本地调试填写127.0.0.1 部署的时候填写为docker-compose redis服务的名称
    redis_port = 6379
    db = 0  # 存储位置
    redis_expire = 86400  # 秒
    BLPOP_TIMEOUT = 10  # 取数超时时间
    pretty_boy_key = "pretty_boy:key"

    group_id = '892473460'
    bot_id = '2522262730'
