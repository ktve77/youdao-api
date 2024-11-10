import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import json
import crawles

url = 'https://dict.youdao.com/webtranslate'

cookies = {
    'OUTFOX_SEARCH_USER_ID': '-312652410@10.108.162.134',
    'OUTFOX_SEARCH_USER_ID_NCOO': '42958927.495580636',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://fanyi.youdao.com',
    'Pragma': 'no-cache',
    'Referer': 'https://fanyi.youdao.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'sec-ch-ua': '\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
}

ci = input("请输入要翻译的中文\n")

data = {
    'i': ci,
    'from': 'auto',
    'to': '',
    'domain': '0',
    'dictResult': 'true',
    'keyid': 'webfanyi',
    'sign': 'f522e5818a8497d9a329a93a522eaa2e',
    'client': 'fanyideskweb',
    'product': 'webfanyi',
    'appVersion': '1.0.0',
    'vendor': 'web',
    'pointParam': 'client,mysticTime,product',
    'mysticTime': '1683270687293',
    'keyfrom': 'fanyi.web',
}

response = crawles.post(url, headers=headers, data=data, cookies=cookies)

def decrypt(decrypt_str):
    key = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
    iv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"

    key_md5 = hashlib.md5(key.encode('utf-8')).digest()
    iv_md5 = hashlib.md5(iv.encode('utf-8')).digest()

    aes = AES.new(key=key_md5, mode=AES.MODE_CBC, iv=iv_md5)
    code = aes.decrypt(base64.urlsafe_b64decode(decrypt_str))
    return unpad(code, AES.block_size).decode('utf8')

decrypted_text = decrypt(response.text)

data_dict = json.loads(decrypted_text)

try:
    trs_list = data_dict["dictResult"]["ce"]["word"]["trs"]
    translations = [item["#text"] for item in trs_list if "#tran" in item]

    print("翻译结果：")
    for tran in translations:
        print(tran)
except KeyError:
    print("无法找到翻译结果，请检查返回的数据结构。")
