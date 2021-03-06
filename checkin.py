import json
import re
import time
import urllib
import requests
import execjs
from bs4 import BeautifulSoup
from collections import namedtuple
import datetime
import ddddocr
import mailsend

encrypt_js_script = "encrypt.js"
configFile = "config.json"
agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36"
urls = {
	"login": "https://authserver.nju.edu.cn/authserver/login",
	"health_history": "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do",
	"check_in": "http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do",
	"captcha": "https://authserver.nju.edu.cn/authserver/captcha.html"
}

def encrypt(password, encrypt_salt):
	with open(encrypt_js_script, 'r') as f: 
		script = ''.join(f.readlines())
	context = execjs.compile(script)
	return context.call('encryptAES', password, encrypt_salt)

def readcode(session):
	r = session.get(urls['captcha'])
	ocr = ddddocr.DdddOcr(show_ad=False)
	res = ocr.classification(r.content)
	return res


def login(session, username, password):
	code = readcode(session)
	r = session.get(urls['login'])
	soup = BeautifulSoup(r.text, 'html.parser')
	input_boxes = soup.find_all('input')
	
	input_info = {}
	for i in input_boxes:
		name, value = i.get('name'), i.get('value')
		if name not in ["username", "password", "captchaResponse", None]:
			input_info[name] = value 
	
	pattern = re.compile(r"var pwdDefaultEncryptSalt = (.*?);", re.MULTILINE | re.DOTALL)
	encrypt_script = str(soup.find("script", text=pattern))
	pwdDefaultEncryptSalt = re.search('pwdDefaultEncryptSalt = "(.*?)";', encrypt_script).group(1)
	headers = {
		'User-Agent': agent,
		'Origin': "https://authserver.nju.edu.cn",
		'Referer': urls['login'],
		'Content-Type': 'application/x-www-form-urlencoded',
		'Connection': 'keep-alive',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
	}

	data = {
		'username': username,
		'password': encrypt(password, pwdDefaultEncryptSalt),
		'captchaResponse': code,
		'lt': input_info["lt"],
		'dllt': input_info["dllt"],
		'execution': input_info["execution"],
		'_eventId': input_info["_eventId"],
		'rmShown': input_info["rmShown"]
	}
	session.post(urls['login'], data=urllib.parse.urlencode(data), headers=headers)
	

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
		location = history['data'][1]['CURR_LOCATION']
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
	if result['code'] == '0' and result['msg'] == '??????':
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
	
	session = requests.Session()
	session.cookies = requests.cookies.RequestsCookieJar()
	session.headers["User-Agent"] = agent
	session.headers["Accept"] = "application/json, text/plain, */*"
	session.headers["Accept-Encoding"] = "gzip, deflate"
	session.headers["Connection"] = "keep-alive"
	session.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
	session.headers["X-Requested-With"] = "com.wisedu.cpdaily.nju"
	session.headers["Referer"] = "http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html"

	assert 'student_id' in info, "Expected infomation `student_id` not found. Check config.json"
	assert "password" in info, "Expected infomation `password` not found. Check config.json"

	login(session, username=info['student_id'], password=info['password'])
	wid, location, status = check_login(session, info['location'])
	if not status:
		return False
	health_status = (
		wid,                                 # WID
		location,                            # ??????
		info['body_temp_ok'],                # ????????????
		info['health_status'],               # ????????????
		info['my_health_code_color'],        # ?????????????????????
		info['fam_mem_health_code_color'],   # ?????????????????????
		info['leave_Nanjing'],               # 14???????????????
		info['last_RNA']                     # ??????????????????
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
			cur_time = datetime.datetime.now().strftime("%Y???%m???%d??? %H???%M???%S???")
			print("failed after try " + str(try_N_times) + " times, " + cur_time)
			mail = mailsend.mailSend("myconfig.json", "??????????????????", "??????????????????????????????????????????????????????" + cur_time)
			mail.sendMsg()