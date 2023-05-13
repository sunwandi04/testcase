import requests

url = 'http://119.23.104.179/project/api/project/auth/v2/login'
payload = {"password": "Test1234", "captcha": "", "email": "marsdev@ones.ai"}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=payload, headers=headers)
# 检查响应状态码
if response.status_code == 200:
    # 响应成功，解析JSON数据
    data = response.json()
    print(data["user"]["token"])

