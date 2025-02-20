[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]  
[![PyPI - Version][pypi-version-shield]][pypi-url]
[![PyPI - PyVersion][pypi-pyversion-shield]][pypi-url]
# TYStream
TYStream is A Python library for Twitch & Youtube Stream Notification.

## 安裝套件
```python
# Windows
pip install tystream

# Linux/MacOS

python3 -m pip install tystream
```

## 註冊API
### Twitch
1. 前往 [Twitch Developers](https://dev.twitch.tv/) 並登入你的帳號，接著點擊右上角的 `Your Console`。
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/8d4137a2-fb1c-4c01-8c1a-a03ea181a1b3)
1. 點選左側欄位的應用程式，再點選 `註冊您的應用程式`。
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/06011479-aa80-4def-a34a-a5f220ad971c)
3. 為你的應用程式取一個自己的名字！其餘的照圖填入並按下`建立`即可。
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/12f4e911-abe4-4367-954f-96cacc44f30a)
4. 回到第三步驟的畫面後，點選剛建立好的應用程式最右側按鈕`管理`再點選最底下的 `新密碼`  底下便會多出`用戶端ID`和`用戶端密碼`兩個欄位的金鑰。  
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/1b8a0c62-31c6-4f00-a456-96c7bf4a46b4)
5. 很好，你已經完成了所有步驟！請將剛拿到的兩組金鑰記好，不要隨意外洩！
### Youtube
1. 前往 [Google Cloud Platform](https://console.cloud.google.com/?hl=zh-tw) 並登入你的帳號。
2. 點選最上方欄位的 `選取專案`，再點選右上角的`新增專案`。
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/ae2bd559-6a55-4bf8-95d4-86b1e46619b8)
3. 按下`建立`後，依照圖片的搜尋方法找到 `YouTube Data API v3`
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/2697cab3-3ce5-412c-85b8-64abfad8f91d)
> [!WARNING]
> 如果這步驟沒有正確啟用，那麼在使用套件的途中就會出現狀況。
4. 點選 `啟用`
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/8fd69240-88db-4d7e-b212-28892b142ade)

5. 啟用完成後，點選左側欄位中的 `憑證`，再點選上方的 `建立憑證`，選擇 `API 金鑰`
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/47666706-c172-4301-a48c-07108e3926c8)
6. 複製彈出視窗的API金鑰，並將此金鑰記下來，大功告成(ﾉ>ω<)ﾉ
![image](https://github.com/Mantouisyummy/TYStream/assets/51238168/1b7c2f35-440d-475e-a2d5-ee4a5125a5ea)

## 如何使用

### Twitch
`client_id` 和 `client_secret` 分別為你在 <a href="#twitch">註冊API教學 (Twitch)</a> 中拿到的 `用戶端ID`和`用戶端密碼`   
`streamer_name` 為 `twitch.tv/...` 後的名稱
### 同步方法
```py
from tystream import Twitch
twitch = Twitch("client_id", "client_secret")
stream = twitch.check_stream_live("streamer_name")
print(stream)
```
### 非同步方法
```py
from tystream.async_api import AsyncTwitch
import asyncio

async def main():
    twitch = AsyncTwitch("client_id", "client_secret")
    stream = await twitch.check_stream_live("streamer_name")
    print(stream)

asyncio.run(main())
```

### Youtube
`api_key` 為你在 <a href="#youtube">註冊API教學 (Youtube)</a> 中拿到的 `API金鑰`  
`streamer_name` 為實況主頻道網址 `https://www.youtube.com/...` 後的名稱 (有無`@`都亦可)
### 同步方法
```py
from tystream import Youtube
youtube = Youtube("api_key")
stream = youtube.check_stream_live("streamer_name")
print(stream)
```
### 非同步方法
```py
from tystream.async_api import AsyncYoutube
import asyncio

async def main():
    youtube = AsyncYoutube("api_key")
    stream = await youtube.check_stream_live("streamer_name")
    print(stream)

asyncio.run(main())
```
<!-- SHIELDS -->

[pypi-pyversion-shield]: https://img.shields.io/pypi/pyversions/tystream?style=for-the-badge

[pypi-version-shield]: https://img.shields.io/pypi/v/tystream?style=for-the-badge&color=green

[pypi-url]: https://pypi.org/project/tystream/

[contributors-shield]: https://img.shields.io/github/contributors/Mantouisyummy/TYStream.svg?style=for-the-badge

[contributors-url]: https://github.com/Mantouisyummy/TYStream/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/Mantouisyummy/TYStream.svg?style=for-the-badge

[forks-url]: https://github.com/Mantouisyummy/TYStream/network/members

[stars-shield]: https://img.shields.io/github/stars/Mantouisyummy/TYStream.svg?style=for-the-badge

[stars-url]: https://github.com/Mantouisyummy/TYStream/stargazers

[issues-shield]: https://img.shields.io/github/issues/Mantouisyummy/TYStream.svg?style=for-the-badge

[issues-url]: https://github.com/Mantouisyummy/TYStream/issues

[license-shield]: https://img.shields.io/github/license/Mantouisyummy/TYStream.svg?style=for-the-badge

[license-url]: https://github.com/Mantouisyummy/TYStream/blob/main/LICENSE.txt
