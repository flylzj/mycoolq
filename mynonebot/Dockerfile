FROM python:3.8-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk update \
    && apk add gcc python3-dev musl-dev libffi-dev build-base

WORKDIR /usr/src/app

COPY req.txt /tmp/
RUN pip3 install -r /tmp/req.txt --no-cache-dir --disable-pip-version-check -i https://pypi.douban.com/simple/

COPY . .

CMD ["python", "bot.py"]
