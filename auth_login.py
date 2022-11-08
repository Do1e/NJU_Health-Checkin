import ddddocr
ocr = ddddocr.DdddOcr(show_ad = False)

import requests
import re
from Crypto.Cipher import AES
import base64

url_authserver = "https://authserver.nju.edu.cn/authserver/"
url_login = url_authserver + "login"
url_captcha = url_authserver + "captcha.html"
url_logout = url_authserver + "logout.do"
url_index = url_authserver + "index.do"

class Auth():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.err_msg = "未知错误"

    def logout(self):
        self.session.get(url_logout, verify=False)
        self.err_msg = "已经退出账号"

    def get_captcha(self):
        r = self.session.get(url_captcha, verify=False)
        captcha = ocr.classification(r.content)
        return captcha
    
    def is_login(self):
        r = self.session.get(url_index, verify=False)
        return "个人资料" in r.text

    def login_mobile(self):

        def encrypt(data, key):

            iv = b'\0'*16
            aes = AES.new(key.encode(), AES.MODE_CBC, iv)
            data = '\0'*64 + data
            
            padding_len = 16 - len(data) % 16 # len(data.encode())
            padding = chr(padding_len)*padding_len

            data = (data + padding).encode()
            data = aes.encrypt(data)
            data = base64.b64encode(data).decode()
            return data

        r = self.session.get(url_login, verify=False)
        pwdDefaultEncryptSalt = re.search("\"pwdDefaultEncryptSalt\" value=\"(.+?)\"", r.text).group(1)
        e1s1 = re.search("\"execution\" value=\"(e\d+?s\d+?)\"", r.text).group(1)
        lt = re.search("LT-.+?-cas", r.text).group()

        data = {
            "username": self.username,
            "password": encrypt(self.password, pwdDefaultEncryptSalt),
            "captchaResponse": self.get_captcha(),
            "dllt": "mobileLogin",
            "lt": lt,
            "execution": e1s1, # 不能去掉
            "_eventId": "submit", # 不能去掉
        }
        r = self.session.post(url_login, data=data, allow_redirects=False, verify=False)
        if "CASTGC" not in r.cookies:
            self.err_msg = re.search("<span.+?auth_error.+?>(.+?)</span>", r.text).group(1)

if __name__ == "__main__":
    username = ""
    password = ""

    auth = Auth(username=username, password=password)
    auth.login_mobile()
    assert auth.is_login() == True
    auth.logout()
    assert auth.is_login() == False
