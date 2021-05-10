import random
import toml
from .config import the_boy, file, data, sex


def check_boy(boys):

    while True:
        boy = random.choice(boys)
        if boy['sex'] != 'unknown':
            the_boy['user_id'] = boy['user_id']
            the_boy['nickname'] = boy['nickname']
            with open(file, 'w', encoding="utf-8") as f:
                r = toml.dump(data, f)
            return sex[boy['sex']], boy['user_id']
        else:
            continue