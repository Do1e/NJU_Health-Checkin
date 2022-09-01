import json
import time
import requests
from collections import namedtuple
import datetime

configFile = "config.json"
urls = {
	"health_history": "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do",
	"check_in": "http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do",
}

def check_login(session, location):
	r = session.get(urls['health_history'])
	try:
		history = json.loads(r.text)
		assert history['code'] == '0'
	except:
		return None, location, False

	print("Log in Successfully")
	wid = history['data'][0]['WID']
	if location == 'default':
		location = history['data'][0]['CURR_LOCATION']
	return wid, location, True


def checkin(session, checkin_info):
	info_t = namedtuple('Checkin_Info', 
		['WID', 'CURR_LOCATION', 'IS_TWZC', 'IS_HAS_JKQK', 'JRSKMYS', 'JZRJRSKMYS', 'SFZJLN', 'ZJHSJCSJ']
	)
	info = info_t._make(checkin_info)
	checkin_url = urls['check_in']+'?'
	for key, value in info._asdict().items():
		checkin_url += f'{key}={value}&'
	checkin_url = checkin_url[:-1]  # drop last &

	r = session.get(checkin_url)
	result = json.loads(r.text)

	cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if result['code'] == '0' and result['msg'] == '成功':
		print("successfully, " + cur_time)
		return True 
	else: 
		print("failed, " + cur_time)
		return False

def main():
	with open(configFile, "r", encoding='utf-8') as f:
		info = json.load(f)
		if info['last_RNA'] == 'default':
			yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
			info['last_RNA'] = yesterday.strftime("%Y-%m-%d+%H")
	assert 'User_Agent' in info, "Expected infomation `User_Agent` not found. Check config.json"
	assert "Cookie" in info, "Expected infomation `Cookie` not found. Check config.json"
	
	session = requests.Session()
	session.headers["Cookie"] = info["Cookie"]
	session.headers["User-Agent"] = info['User_Agent']
	session.headers["Accept"] = "application/json, text/plain, */*"
	session.headers["Accept-Encoding"] = "gzip, deflate"
	session.headers["Connection"] = "keep-alive"
	session.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
	session.headers["X-Requested-With"] = "com.wisedu.cpdaily.nju"
	session.headers["Referer"] = "http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html"

	wid, location, status = check_login(session, info['location'])
	if not status:
		return False
	health_status = (
		wid,                                 # WID
		location,                            # 地点
		info['body_temp_ok'],                # 体温正常
		info['health_status'],               # 健康状况
		info['my_health_code_color'],        # 本人苏康码颜色
		info['fam_mem_health_code_color'],   # 家人苏康码颜色
		info['leave_Nanjing'],               # 14天是否离宁
		info['last_RNA']                     # 上次核酸时间
	)
	return checkin(session, health_status)
	

if __name__ == '__main__':
	result = main()
	if not result:
		with open(configFile, "r", encoding='utf-8') as f:
			info = json.load(f)
		if 'try_N_times' in info:
			try_N_times = int(info['try_N_times'])
		else:
			try_N_times = 10
		N = try_N_times
		while(not result and N > 0):
			time.sleep(120)
			result = main()
			N -= 1
		if not result:
			cur_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H点%M分%S秒")
			print("failed after try " + str(try_N_times) + " times, " + cur_time)