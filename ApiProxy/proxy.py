import glob
import json
import subprocess
import os
import platform
from threading import Thread
import time
import requests
import atexit
class Proxy():
    """
    代理类
    """
    system_list={"Windows":"win", "Linux":"linux", "Darwin":"mac"}
    def __init__(self, port:int=0,porxy_port:int=0):
        self.port =port 
        self.port_proxy = porxy_port
        self.baseurl=f"http://127.0.0.1:{self.port}"
        self.process=None
        self.isflag=False
        self._th=Thread(target=self._init_proxy,daemon=True)
        self.start()
        # self._init_proxy()
    def setproxyIp(self,proxyurl:str="") ->dict:
        """
        设置上游代理url\n
        :param proxyurl 代理url,不填,则使用系统网络直连\n
        :return dict 返回结果,其中url是返回的http代理链接\n
        ps:首次必须调用此方法获取转为http代理链接的url\n
        """
        if not proxyurl:
            raise RuntimeError("代理url不能为空")
        data=self._sendrequest("start",url=proxyurl)
        self.isflag=True
        print(data)
        return data
    def switchproxyIp(self,proxyurl:str="") ->bool:
        """
        动态切换代理ip\n
        :param proxyurl 代理url\n
        :return bool 返回结果\n
        ps:调用此方法前提必须调用了setproxyIp方法,后续才能用此方法动态切换ip
        """
        # 避免代理端口占用
        if self.isflag:
            self.stopProxy()
            data=self._sendrequest("start",url=proxyurl)
            if data.get("code",-1)==0:
                return True
            else:
                return False
        else:
            return False  
        
    def stopProxy(self) ->dict:
        """
        停止代理\n
        :return dict 返回结果\n
        """
        data=self._sendrequest("close")
        # print("打印响应结果：",data)
        return data
    def _hook_exitHandler(self):
        try:
            if self.process:
                self.terminate()
            else:
                self.killsearchName(self.getexecuteName(self._getexecuteFile()))
            # print("杀掉进程")
        except:
            pass
        # print("程序退出")
    def _init_proxy(self):
        """
        初始化代理
        """
        print("初始化代理")
        executable_path=self._getexecuteFile()
        shell=[executable_path]
        if self.port != 0:
            shell.append(f'--port={self.port}')
        if self.port_proxy != 0:
            shell.append(f'--proxy_port={self.port_proxy}')
        self.process=subprocess.Popen(shell,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if self.process.pid >=0:
            print(f"代理服务启动成功,进程id:{self.process.pid},http端口:{self.port},代理端口:{self.port_proxy}")
        # 等待程序执行完成
        # stdout, stderr = self.process.communicate()
        self.process.communicate()
        if self.process.returncode != 0:
            # 如果返回码非0，表示程序有错误发生
            # raise RuntimeError(f"代理启动失败:{stderr.decode()}")
            pass
    def start(self):
        # 启动线程
        atexit.register(self._hook_exitHandler)
        self._th.start()
        # self._th.join(timeout=6)
    def terminate(self):
        """
        终止当前代理进程
        """
        if self.process:
            self.process.kill()
            print("代理自动销毁")
    def killsearchName(self,name:str):
        """
        根据进程名称进行终止
        """
        p=subprocess.Popen('taskkill /f /im {}'.format('apiproxy.exe'),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait(2)

    def getexecuteName(self,executable_path:str) ->str:
        """
        根据程序路径获取当前进程名称
        """
        if not executable_path:
            raise RuntimeError("未找到程序路径")
        name=os.path.basename(executable_path)
        return name
    def __del__(self):
        """
        类销毁时执行,销毁代理
        """
        pass
        # self.terminate()
           
    def _getexecuteFile(self) ->str:
        """
        获取执行文件路径
        """
        __file_path=os.path.abspath(__file__)
        data_files = {}
        directories = glob.glob(os.path.join(os.path.dirname(__file_path), "dependencies/*"))
        for directory in directories:
            if "exe" in directory:
                data_files["win"]=directory
            elif "linux" in directory:
                data_files["linux"]=directory
            elif "mac" in directory:
                data_files["mac"]=directory
        
        if len(data_files)<=0:
            raise RuntimeError("未找到依赖文件")
        system_name = platform.system()
        system_name=self.system_list.get(system_name,"")
        executable_path=data_files.get(system_name,None)
        if executable_path is None:
            raise RuntimeError("未找到依赖文件")
        return executable_path
    def _sendrequest(self,_method:str,**kwargs)->dict:
        """
        与代理服务器进行通信\n
        :param _method 请求方法\n
        :param kwargs 请求参数\n
        :return dict 返回结果
        """
        header={
            "Content-Type":"application/json"
        }
        data=json.dumps(kwargs)
        url=f"{self.baseurl}/{_method}"
        response=requests.post(url,headers=header,data=data)
        return response.json()
if __name__ == "__main__":
    a=Proxy(8993,8996)
    a.setdynamicProxy("socks://127.0.0.1:10808")
    # print(a._getexecuteFile())
    while True:
        try:
            time.sleep(1)
            
            print("测试")
        except KeyboardInterrupt:
            break



