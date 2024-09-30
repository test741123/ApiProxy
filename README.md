# 快捷使用
## 安装库
- pip install ApiProxy

## 编译库
- python ./setup.py sdist bdist_wheel 
- pip install .\ApiProxy-1.0-py3-none-any.whl

## 上传库
- twine upload dist/*

## 卸载库
- pip uninstall ApiProxy

## 场景1-设置dp代理,支持socks代理

```
from DrissionPage import ChromiumPage,ChromiumOptions

from ApiProxy import Proxy

a=Proxy(8993,8996)

data=a.setproxyIp("http://183.158.146.144:40023")

proxyurl=data["url"]

print("proxyurl:",proxyurl)

co=ChromiumOptions()

co.set_proxy(proxyurl)

page=ChromiumPage(addr_or_opts=co)

page.get("https://www.baidu.com")

input("等待输入")
```

## 场景2-使用dp动态代理切换,支持socks代理

```
from DrissionPage import ChromiumPage,ChromiumOptions
from ApiProxy import Proxy
a=Proxy(8993,8996)
data=a.setproxyIp("http://183.158.146.144:40023")
proxyurl=data["url"]
print("proxyurl:",proxyurl)
co=ChromiumOptions()
co.set_proxy(proxyurl)
page=ChromiumPage(addr_or_opts=co)
page.get("https://www.ip138.com")
input("第一次切换ip")
# 再次切换代理
a.switchproxyIp("http://49.87.97.136:40007")
page.get("https://www.ip138.com")
input("第二次切换ip")
```
# 接下来计划
## 重构apiproxy，使apiproxy支持代理链,sock5代理，全局上游代理，动态更换代理，以及对指定url进行切换代理
## 支持tls随机指纹
## 支持整个代理端的所有接口监听，比起dp原生监听不会存在多个嵌套页面接口漏的情况

