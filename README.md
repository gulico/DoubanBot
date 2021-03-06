# DoubanBot

豆瓣自动回帖机器人（多组）

### 使用方法

* 安装 requirements：```pip3 install -r requirements.txt```

* 抓包，在```config.py```里填入需要设置的值
* 启动IP代理池：```python3 IPProxyPool/IPProxy.py``` （需要一直在后台运行）
* 运行主程序：```python3 autoreply.py```

### 特点

1. 相比爬虫豆瓣网页版并回复的优势：没有验证码，并且利用的是豆瓣现成的API接口
2. 可以多组回复，不过抓包的时候每个组的sig和ts都需要更新，否则可能状态码可能会报400
3. 因为使用的小组的特点，还增加了一点特定时间特定回复的设置，且有休息时间。不想要的可以注释掉。

### 展望

1. 最近看了一下可以接图灵机器人之类的接口，回复应该可以更机智一点。主要是我面向的人群比较特殊，不知道自定义的语料库够不够用，以及公共的语料库会不会不适用。
2. 现在多组回复的情况下就是有点延迟，漏回复的情况比较多，不知道能不能改善。