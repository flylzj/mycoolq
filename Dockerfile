FROM ubuntu:16.04
RUN apt-get update && apt-get install -y \
    python3 python3-dev build-essential python3-pip libssl-dev\
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoclean
COPY ./req.txt /tmp/
RUN pip3 install -r /tmp/req.txt --no-cache-dir --disable-pip-version-check -i https://pypi.douban.com/simple/

ENV TZ=Asia/Shanghai
ENV FLASK_CONFIG=production
ENV LANG=C.UTF-8

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir /app
WORKDIR /app

EXPOSE 8888
CMD ["python3", "bot.py"]
