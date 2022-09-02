# NJU_Health-Checkin

---
2022-09-02: 更新适用于最新的统一身份认证安全登录
---

**使用方法**

* 在config.json中填写`student_id`、`password`、上次核酸时间(default表示默认昨天做的核酸)、打卡地点(default表示默认昨天的打卡地点，因此地点更新只需在手机上手动打卡一次即可)
* 运行`python checkin.py`即可完成打卡一次
* 若要每天12:00自动运行，请在`contab -e`中添加以下命令：`0 12 * * * cd /path/to/checkin && python checkin.py >> checkin.log 2>&1`
* 或自行查找如何设置Windows下的定时任务

**Github Actions**
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
* 注：最近14天是否离宁由程序自动检测最近14天的打卡地址是否含有'南京市'字符串
* **last_RNA**：您的最近一次核酸检测时间，"default"表示默认昨天做的核酸，格式如下："2022-09-01+16"，即2022年9月1日16点
* **try_N_times**：若打卡失败的重试次数，不写为默认为3次

:rotating_light:**请务必如实上报健康状况**，如有异地出行、身体状况变动、本人或家人健康码非绿色，请停止使用此脚本。

### 参考&感谢

[yegcjs/NJU_Health-Checkin](https://github.com/yegcjs/NJU_Health-Checkin)  
