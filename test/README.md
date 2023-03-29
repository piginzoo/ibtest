# 说明

这个是ib的测试程序。

- main.py 获得各类数据
- get_option_chain.py 用ib官方api获得期权链
- get_option_chain_by_ib_sync.py 用三方的ib_sync来获得期权链

# 如何运行

先要安装[ib官方包](../sdk/)，和ib_sync

1、安装官方的sdk，需要自己编译和安装，参考[README.md](../sdk/README.md)：

* you can use this to build a source distribution

`python3 setup.py sdist`

* you can use this to build a wheel

`python3 setup.py bdist_wheel`

* you can use this to install the wheel

`python3 -m pip install --user --upgrade dist/ibapi-9.75.1-py3-none-any.whl`

2、安装ib_sync：'pip install ib_sync'

3、运行

```commandline
python main.py
python get_option_chain.py
python get_option_chain_by_ib_sync.py
```

4、报错处理

会报错说eventkit找不到，`pip install eventkit`后，还是报错说找不到。
```commandline
Traceback (most recent call last):
  File "/Users/piginzoo/workspaces/ibgw/test/test3.py", line 2, in <module>
    from ib_insync import *
  File "/Users/piginzoo/softwares/py3/lib/python3.9/site-packages/ib_insync/__init__.py", line 6, in <module>
    from eventkit import Event
ModuleNotFoundError: No module named 'eventkit'
```
这个时候，需要进入到site-packages目录下，然后把`eventKit`目录改名成`eventkit`。