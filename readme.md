# 我的coolq机器人

## ~~基于[酷Q](https://cqp.cc/) [coolq-http-api](https://github.com/richardchien/coolq-http-api) [nonebot](https://github.com/richardchien/nonebot) 的机器人~~
## 基于 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) [nonebot](https://github.com/nonebot/nonebot) 的qq机器人


### 目前有的功能

- [x] 骰子
- [x] 定时t人
- [x] 加群验证码
- [x] 查询python标准库文档


### 开发

*克隆代码*
```shell script
git clone https://github.com/flylzj/mycoolq.git
```

*安装并创建python虚拟环境*
```shell script
pip install virtualenv
\venv\Scripts\activate.bat
```

*安装依赖*
```shell script
pip install -r req.txt
```

*开发插件*

在`coolq/plugins`目录下新建文件夹，文件名为插件名即可

具体可参考[https://docs.nonebot.dev/guide/command.html](https://docs.nonebot.dev/guide/command.html)
