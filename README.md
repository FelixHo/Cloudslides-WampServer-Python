Cloudslides-WampServer
======================

Cloudslides-WampServer-Python

运行环境部署:

1.python 2.7.6 安装见https://www.python.org/ 

2.安装pip 见https://pip.pypa.io/en/latest/installing.html

3.安装twisted 见https://twistedmatrix.com/trac/

4.安装twisted的依赖 zope4.1.1 https://pypi.python.org/pypi/zope.interface#download

5.安装autobahn模块 命令行执行 cd path/to/pip.exe install autobahn

6.安装pymongo模块（2.7.1） 见https://pypi.python.org/pypi/pymongo/#downloads


测试数据库部署: 

WampServer目前基于本地数据库测试，需要在本地部署一个mongo数据库【 必须基于原liveppt数据库结构，数据库重命名为Cloudslides,原因参见代码配置 https://github.com/FelixHo/Cloudslides-WampServer-Python/blob/master/src/wamp/PageController.py#L59 】
（将原liveppt的msql数据库转为mongodb，可通过MongoVUE或类似的mongo GUI工具实现）。


运行

Server端:

python PageController.py

测试Client【获取某会议的当前页码，根据返回的topic进行订阅，每隔5秒翻一页，基于python实现】:

python ClientTest.py


接口文档

https://github.com/FelixHo/Cloudslides-WampServer-Python/tree/master/doc
