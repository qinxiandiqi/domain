#domain

功能：<br>
Python脚本自动化查询还没被注册的域名。<br>

使用方法：<br>
1.直接运行domain.py<br>
2.可选参数：<br>
-n 或 --name ：查询指定域名<br>
-d 或 --domain ：自动化查询域，默认查询com域。<br>
-f 或 --file ：自动化查询结果保存文件名，默认以所查询域作为文件名。<br>
-p 或 --prefix ：添加自动化查询域名前缀，默认不添加。<br>
-s 或 --suffix ：添加自动化查询域名后缀，默认不添加。<br>
-m 或 --max ：自动化查询生成域名最长长度，默认为5。<br>
-l 或 --log ：是否打印已被注册域名日志，默认不打印。<br>
-t 或 --timesleep ：自动化查询速度过快遭服务器拒绝时的休眠时间，默认为30秒。<br>
--timestep ：连续自动化查询速度过快遭服务器拒绝时，休眠时间增长步长，默认为5秒。<br>
-e 或 --eachsleep ：为避免查询过快遭服务器拒绝，每次查询休眠间隔时间，默认为1秒。<br>
3.运行过程中可以按Ctrl+C终止查询。<br>

测试环境：<br>
Python2.7测试通过。<br>

# License

    Copyright 2015 Jianan - qinxiandiqi@foxmail.com

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
