Bug-Project-Framework
======================

时间过去这么久了，感觉框架也该升级了，回过头看，这个太垃圾了。
今后框架主体不会再更新优化，仅做模块更新，供广大安全爱好者做漏洞复现记录利用使用。
由于受到相关法律法规和其他政策的影响，新制框架不会对公众开放下载使用，谢谢理解。

[+]简介：
---------
	*允许使用者使用BPF框架语言
	*允许自行扩充EXP
	*可通过框架快速检测安全漏洞是否存在
	*对相应的网络环境进行安全审计工作


[+]检测对象：
---------------
	*互联网虚弱目标


[+]使用说明：
---------------
	*框架启动前请尽量关闭杀软或暂停文件保护服务，杀毒软件会误杀框架组件，导致框架失效；
	*第一次使用前，请将全部文件解压到一个固定路径的文件夹，然后打开shellcode options修改shellcode路径；
	*然后将exploit放在相应的文件夹内，exploit类放在exploit文件夹内，poc类放在poc文件夹内，buffer类放在buffer文件夹内，启动框架，即可使用相应功能；

	*exploit类主要针对WEB漏洞，poc类主要针对WEB漏洞检测，buffer类调用外置可执行模块。

[+]使用方法：
------------------

    在BPF根命令行下：

          help                查询帮助

          reload              重新加载框架，此时会刷新全部模块

          search              搜索模块关键词并显示
                              （ e.g.  search ms17-010 ）
          searchall           显示所有模块

          use                 使用模块
                              （ e.g.  use \buffer\ms17-010 Scan.bpf ）
          set shellcodes      配置默认Shellcode路径

          exit                退出BPF


    在BPF模块命令行下：

          help                查询帮助

          show options        查看当前模块参数以及配置情况

          set options         设置当前模块参数以及配置

          set shellcodes      配置默认Shellcode路径

          run                 运行模块

          exit                退出当前模块

    当你输入除上述指定规定参数以外的命令时，BPF框架会将命令识别为系统命令，提交Windows操作系统进行处理

          HAPPY HACK ！GOOD LUCK ！
          2018.5.7 BY Fplyth0ner

[+]使用截图
-------------
![One](https://github.com/Fplyth0ner-Combie/Bug-Project-Framework/blob/master/images/1.jpg)
![Two](https://github.com/Fplyth0ner-Combie/Bug-Project-Framework/blob/master/images/2.jpg)

[+]exploit编写：
----------------
	*框架自带编写记事本，可参考BPF语法快速编写exploit，详情请参考BPF IDE提示的语法。


[+]感谢：
---------------
	Metasploit - Rapid7
	NetCat - Hobbit

[+]铭恩：
-----------
	Computer - John von Neumann
	Internet - Tim Berners-Lee
	Linux - Linus Benedict Torvalds
	Windows - Bill Gates
	C - D.M.Ritchie
	JavaScript - Brendan Eich
	Tomcat - James Duncan Davidson
	Apache - Apache Software Foundation
	Java - James Gosling
	VMware - Diane Greene
	Baidu - 李彦宏
	Google - Larry Page


[+]特别感谢：
-------------
	Tencent - 马化腾
	E - 吴涛

---------------------------------
2017年4月12日工程  -- Fplyth0ner

欢迎大家积极参与模块编写计划！

---------------------------------
