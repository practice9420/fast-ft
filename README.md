# fast-ft（Fast File Transfer）

fast-ft 是一个精简的文件传输工具，做到安装即用，无需任何配置，操作简单快捷，是开发者局域网内文件传输的好帮手。

Fast-ft is a simple file transfer tool, which can be installed and used without any configuration. It is a good helper for developers to transfer files in LAN.

精简，精简到两个页面，一个上传一个下载，做传输工具最重要的目标是稳定可靠的实现传输。

Simplify, simplify to two pages, one upload and one download, the most important goal of transmission tool is stable and reliable transmission.

便捷，无需任何配置操作，只要电脑中有python，在全局安装一个包就可以在命令行中快速启动网站，网站首页自动打开，提供二维码供其他移动设备快速访问。

Convenient, without any configuration operation, as long as there is Python in the computer, you can quickly start the website in the command line by installing a package in the global, and the homepage of the website will automatically open, providing two-dimensional code for other mobile devices to quickly access.

缓解，开发者不再需要依赖社交应用（QQ、微信)来完成局域网内文件传输，也不用因为找不到数据线这种传统介质而着急上火，只要你电脑里安装了python就能非常方便的传输文件。

Ease, developers no longer need to rely on social applications (QQ, wechat) to complete the file transfer within the LAN, and they don't need to be anxious because they can't find the traditional media such as data cable. As long as you install Python in your computer, you can easily transfer files.




## 运行（run）

* ```shell
  # 拉取github源码 运行
  # Pull GitHub source code to run.
  git clone https://github.com/practice9420/fast-ft.git
  cd fast_ft
  pip install -r requirements
  python server.py
  ```

* ```shell
  # 安装工具包 建议使用清华大学镜像站（据我感受清华大学镜像站同步频率最高）
  # The installation kit recommends using Tsinghua University mirror station (as far as I feel, Tsinghua University mirror station has the highest synchronization frequency).
  pip install fast-ft -i https://pypi.tuna.tsinghua.edu.cn/simple/
  fast-ft
  ```

* 



## 效果（effect）

* [bilibili效果演示](https://www.bilibili.com/video/BV1SK4y1D7Zt)



## 技术（technology）

* Python Web Framework Flask.
* html UI library bootstrap.
* Webuploader, a fragment upload plug-in.



## 未来（future）

* 或许将会考虑加入用户角色，实现口令访问私密空间。
* Maybe we will consider adding user roles to achieve password access to private space.
* 基于用户角色开发局域网内公共、私有聊天室，能够快速将自己访问口令传输给其他人。
* The public and private chat rooms in LAN are developed based on the user role, which can quickly transfer their access password to other people.
* 传输性能优化，如果有更好的实现方案我肯定会去尝试，前提是我知道。这些设想全都建立在有人使用的基础之上，如果没有人是用完全没有必要做更多的功能。
* Transmission performance optimization, if there is a better implementation scheme, I will certainly try, provided that I know. These ideas are all based on the use of some people. If no one uses them, there is no need to do more functions.

## 致谢（thank）

* [感谢开源项目](https://github.com/lsm1103/pyupload)

## 版本说明

> fast-ft 0.1.1
>
> ```
> 1.加入聊天大厅。
> ```
>
> fast-ft 0.1.2
>
> ```
> 1.修复聊天大厅发送代码后样式错乱；
> 2.添加每条消息copy复制按钮；
> 3.首页点击聊天大厅logo跳转聊天大厅单独页面；
> 4.聊天大厅单独页面点击logo跳转到首页;
> 5.项目根目录加入到sys.path环境变量。
> ```
>
> 

