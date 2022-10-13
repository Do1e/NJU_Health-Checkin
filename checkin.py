import json
import time
from collections import namedtuple
import datetime

from auth_login import Auth

configFile = "config.json"
urls = {
	"health_history": "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do",
	"check_in": "http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do",
}

def check_login(session, location, leave_NJ):
	r = session.get(urls['health_history'])
	try:
		history = json.loads(r.text)
		assert history['code'] == '0'
	except:
		return None, location, False

	print("Login Successfully")
	wid = history['data'][0]['WID']
	if location == 'default':
		try:
			location = history['data'][1]['CURR_LOCATION'] # 与昨天的CURR_LOCATION保持一致
		except:
			print('由于昨天没有打卡，无法获取默认打卡地点。请手动设置')
			exit(-1)
	if leave_NJ == 'default':
		leaveNanjing = False
		for i in range(1,14):
			try:
				nowL = history['data'][i]['CURR_LOCATION']
			except:
				continue
			if '南京市' not in nowL:
				leaveNanjing = True
				break
	else:
		leaveNanjing = False if leave_NJ == '0' else True
	return wid, location, leaveNanjing


def checkin(session, checkin_info):
	cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	info_t = namedtuple('Checkin_Info', 
		['WID', 'CURR_LOCATION', 'IS_TWZC', 'IS_HAS_JKQK', 'JRSKMYS', 'JZRJRSKMYS', 'SFZJLN', 'ZJHSJCSJ']
	)
	info = info_t._make(checkin_info)
	checkin_url = urls['check_in']+'?'
	for key, value in info._asdict().items():
		checkin_url += f'{key}={value}&'
	checkin_url = checkin_url[:-1]  # drop last &

	r = session.get(checkin_url)
	try:
		result = json.loads(r.text)
	except:
		print("failed, " + cur_time)
		print(r.text)
		return False

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
			timeZone = time.strftime('%Z', time.gmtime())
			assert timeZone[:2] == '中国' or timeZone[:5] == 'China' or timeZone[:3] == 'GMT', '本机时区无法转换，请在github(https://github.com/Do1e/NJU_Health-Checkin)提交issue'
			if timeZone[:2] == '中国' or timeZone[:5] == 'China':
				yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
			else:
				yesterday = datetime.datetime.now() - datetime.timedelta(days=1) + datetime.timedelta(hours=8)
			info['last_RNA'] = yesterday.strftime("%Y-%m-%d+%H")
			print('waining: 上次核酸时间未设置，默认为: ' + info['last_RNA'])
	assert 'student_id' in info, "Expected infomation `User_Agent` not found. Check config.json"
	assert 'password' in info, "Expected infomation `Cookie` not found. Check config.json"
	assert 'User_Agent' in info, "Expected infomation `User_Agent` not found. Check config.json"
	assert 'location' in info, "Expected infomation `location` not found. Check config.json"
	assert 'body_temp_ok' in info, "Expected infomation `body_temp_ok` not found. Check config.json"
	assert 'health_status' in info, "Expected infomation `health_status` not found. Check config.json"
	assert 'my_health_code_color' in info, "Expected infomation `my_health_code_color` not found. Check config.json"
	assert 'fam_mem_health_code_color' in info, "Expected infomation `fam_mem_health_code_color` not found. Check config.json"
	assert 'leave_NJ' in info, "Expected infomation `leave_NJ` not found. Check config.json"
	assert 'last_RNA' in info, "Expected infomation `last_RNA` not found. Check config.json"

	auth = Auth(info['student_id'], info['password'])
	auth.login_mobile()
	if not auth.is_login():
		print(auth.err_msg)
		return False
	session = auth.session
	session.headers["User-Agent"] = info['User_Agent']
	session.headers["Accept"] = "application/json, text/plain, */*"
	session.headers["Accept-Encoding"] = "gzip, deflate"
	session.headers["Connection"] = "keep-alive"
	session.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
	session.headers["X-Requested-With"] = "com.wisedu.cpdaily.nju"
	session.headers["Referer"] = "http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html"

	wid, location, leaveNanjing = check_login(session, info['location'], info['leave_NJ'])
	if wid is None:
		return False
	info['leave_Nanjing'] = '1' if leaveNanjing else '0'
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
	status = checkin(session, health_status)
	auth.logout()
	return status
	

if __name__ == '__main__':
	result = main()
	if not result:
		with open(configFile, "r", encoding='utf-8') as f:
			info = json.load(f)
		if 'try_N_times' in info:
			try:
				try_N_times = int(info['try_N_times'])
			except ValueError:
				try_N_times = 0
		else:
			try_N_times = 0
		N = try_N_times
		while(not result and N > 0):
			time.sleep(120)
			result = main()
			N -= 1
		if not result:
			cur_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H点%M分%S秒")
			print("failed after try " + str(try_N_times) + " times, " + cur_time)
			exit(1)
