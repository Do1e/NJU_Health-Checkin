import ddddocr
ocr = ddddocr.DdddOcr(show_ad = False)

import requests
import re
from Crypto.Cipher import AES
import base64

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

url_authserver = "https://authserver.nju.edu.cn/authserver/"
url_login = url_authserver + "login"
url_captcha = url_authserver + "captcha.html"
service = "https://authserver.nju.edu.cn/authserver/mobile/callback?appId=301317066"
url_service = f"{url_login}?service={service}"
url_cpdaily_login = "https://mobile.campushoy.com/v6/auth/authentication/notcloud/login"
CpdailyInfo = "XvWN4SWqyX648L13hW5koOHt5AfBN6jFTi4zR23WludYuPZfzB8fDXe4zUu+ U2kCbakEyBTxeW3f0hd9FPA5f1WlaN2n85/wugOANJTBEcZ7CmPce1z7sTFm VWNC6TSLhTYGMMmSBF8Mn6RrhgfKli+ojtqGHjnfc2FPd5sBgQwQDZRI0gSy /4jez8zcK40QTGAu/F6jLGjljx5L4BnTLQ=="

class Auth():

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.session = requests.Session()
        self.get_login_init()

    def get_login_init(self):
        try:
            r = self.session.get(url_service, timeout=0.5) # 随即地发生超时错误
        except Exception:
            print("get_login_init超时，请重试")
        self.pwdDefaultEncryptSalt = re.search("\"pwdDefaultEncryptSalt\" value=\"(.+?)\"", r.text).group(1)
        self.e1s1 = re.search("\"execution\" value=\"(e\d+?s\d+?)\"", r.text).group(1)
        self.lt = re.search("LT-.+?-cas", r.text).group()

    def get_captcha(self):
        r = self.session.get(url_captcha)
        captcha = ocr.classification(r.content)
        return captcha

    def login_mobile(self):
        data = {
            "username": self.username,
            "password": encrypt(self.password, self.pwdDefaultEncryptSalt),
            "captchaResponse": self.get_captcha(),
            "dllt": "mobileLogin",
            "lt": self.lt,
            "execution": self.e1s1, # 不能去掉
            "_eventId": "submit", # 不能去掉
        }
        r = self.session.post(url_service, data=data, allow_redirects=False)
        if r.status_code == 302 and "CASTGC" in r.cookies:
            location = r.headers["Location"]
            r = requests.get(location, allow_redirects=False)
            location = r.headers["Location"]
            ticket = re.search("mobile_token=(.+)$", location).group(1)
            self.callback_cpdaily(ticket)
            return True
        else:
            return False # 可能是因为验证码识别错误，可能有其他未知原因。
    
    def callback_cpdaily(self, ticket):
        data = {
            "tenantId": "nju", # 不能去掉
            "ticket": ticket
        }
        headers = {
            "CpdailyInfo": CpdailyInfo # 不能去掉
        }
        r = self.session.post(url_cpdaily_login, json=data, headers = headers, allow_redirects=False)
        self.CASTGC = r.json()["data"]["tgc"]
        self.app_session_token = r.json()["data"]["sessionToken"]

if __name__ == "__main__":
    username = ""
    password = ""

    auth = Auth(username=username, password=password)
    auth.login_mobile()
    print(auth.CASTGC)
    print(auth.app_session_token)