# NJU_Health-Checkin

---
2022-11-13 15: 新增配置文件选择，可部署多个账号；使用[NJUlogin](https://github.com/Do1e/NJUlogin)库进行登录  
2022-11-04 22: Github Action抽风，更改了一下Python版本，现在可以正常运行了  
2022-10-29 11: 新增核酸时间配置，新增支持数字格式，表示在打卡时间前`x`小时做了核酸，默认为24  
2022-10-19 11: 增加时区获取以保证"昨天"的计算方法在不同平台上的正确性  
2022-09-27 17: 增加并修复14天内离宁选项控制，修复研究生学号长度为10的问题，感谢 [@Coegle](https://github.com/Coegle) 的PR  
2022-09-03 18: 修复部分同学学号长度为12的问题，感谢 [@i-Pear](https://github.com/i-Pear) 的PR  
2022-09-02 18: 已修复登录问题，感谢 [@log2dx](https://github.com/log2dx) 的PR  
2022-09-02 16: 似乎还存在问题，暂时还没有修复  
2022-09-02 11: 更新适用于最新的统一身份认证安全登录
---

**使用方法**

* 在config.json中填写`student_id`、`password`、`User_Agent`(见抓包方法)、上次核酸时间(default表示默认昨天做的核酸)、打卡地点(default表示默认昨天的打卡地点，因此地点更新只需在手机上手动打卡一次即可)，其中student_id、password为**必须修改的项目**，其余的可以使用config.json中的默认值，具体介绍见config.json解析
* 运行`python checkin.py`即可完成打卡一次
* 或者`python checkin.py -c config.json`来选择指定的配置文件
* 若要每天12:00自动运行，请在`crontab -e`中添加以下命令：`0 12 * * * cd /path/to/checkin && python checkin.py >> checkin.log 2>&1`
* 或自行查找如何设置Windows下的定时任务

**Github Actions**

:rotating_light:**注意，在Github Actions运行时请勿修改`config.json`，否则会造成信息泄露并且！无效！，所有的修改请使用secret**

* 右上角fork本仓库，之后点击`Create fork`

![1662048592065](image/README/1662048592065.png)

* 在自己的仓库中点击 Settings -> Secrets -> Actions -> New repository secret

![1662048748666](image/README/1662048748666.png)

* 对config.json中的每一项进行都新建一个secret(student_id、password为**必填项**，其余默认值见config.json)。自动转换为大写是正常现象

![1662088555802](image/README/1662088555802.png)
![1662096230714](image/README/1662096230714.png)

* 点击 Actions -> I understand

![1662048939547](image/README/1662048939547.png)

* 最后Enable Actions即可，每天中午12:00自动运行，或修改`.github/workflows/checkin.yml`中的`cron`字段来修改运行时间

![1662049002323](image/README/1662049002323.png)

**config.json解析**

* **student_id**：学号
* **password**：统一身份认证密码
* **location**：打卡地址，"default"表示默认昨天的打卡地点，因此地点更新只需在手机上手动打卡一次即可，或者直接使用字符串表示打卡地点，如"江苏省南京市栖霞区九乡河东路159号"
* **body_temp_ok**：您的体温是否正常
* **health_status**：您的其他健康情况
* **my_health_code_color**：您今日的苏康码显示颜色
* **fam_mem_health_code_color**：您共同居住人今日的苏康码显示颜色
* **leave_NJ**：最近14天是否离宁，"default"表示由程序自动检测最近14天的打卡地址是否含有'南京市'字符串，"0"表示否，"1"表示是
* **last_RNA**：您的最近一次核酸检测时间，两种设置格式：1. "2022-09-01+16"，即2022年9月1日16点；2. 纯数字，如"24"表示在打卡时间前24小时做了核酸
* **try_N_times**：若打卡失败的重试次数，不写为默认0(不重试)
* **infection_status**：感染状态，"1","2","3" 分别表示"一直阴性"，"已转阴"，"阳性"

**抓包方法**

* 在电脑上下载[WireShark](https://www.wireshark.org/#download)，并安装
* 打开电脑热点，手机连接上

![1662040547198](image/README/1662040547198.png)

* 打开cmd，输入`ipconfig`，找到IPv4地址为192.168.XX.1(XX为1~255之间的任意数字都可)的连接，记下其名字，如“本地连接\*12”

![1662040857089](image/README/1662040857089.png)

* 手机打开打卡界面，填入信息但暂时不点击“提交”
* 打开WireShark，找到之前记下的连接名字

![1662041047834](image/README/1662041047834.png)

* 双击这个连接，之后手机马上点击“提交”并确定，此时WireShark会进行抓包，此时点击“停止捕获分组”

![1662041181671](image/README/1662041181671.png)

* 在搜索框中输入"http"，之后回车
* 找到包含下图中红框中的项目，单击它

![1662041435032](image/README/1662041435032.png)

* 在下面的窗口展开`Hypertext Transfer Protocol`，便可以找到需要填入的`User_Agent`，右击，复制值，粘贴进config.json中即可(注意json中的引号不要删掉了)

![1662041538194](image/README/1662041538194.png)

![1662041793462](image/README/1662041793462.png)

:rotating_light:**请务必如实上报健康状况**，如有异地出行、身体状况变动、本人或家人健康码非绿色，请停止使用此脚本。

### 参考&感谢

[yegcjs/NJU_Health-Checkin](https://github.com/yegcjs/NJU_Health-Checkin)  
