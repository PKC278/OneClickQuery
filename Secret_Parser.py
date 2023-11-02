import os

api_key = os.environ.get("API_KEY")
baiduocr_api_key = os.environ.get("BAIDUOCR_API_KEY")
baiduocr_secret_key = os.environ.get("BAIDUOCR_SECRET_KEY")
tk_token = os.environ.get("TK_TOKEN")

with open("ocr/main.py", "r", encoding="utf-8") as f:
    config = f.read()
    config = config.replace('api_key = ""', f'api_key = "{api_key}"')
    config = config.replace('tk_token = ""', f'tk_token = "{tk_token}"')

with open("ocr/main.py", "w", encoding="utf-8") as f:
    f.write(config)
    f.close()

with open("ocr/BaiduOCR.py", "r", encoding="utf-8") as f:
    config = f.read()
    config = config.replace('API_KEY = ""', f'API_KEY = "{baiduocr_api_key}"')
    config = config.replace('SECRET_KEY = ""', f'SECRET_KEY = "{baiduocr_secret_key}"')

with open("ocr/BaiduOCR.py", "w", encoding="utf-8") as f:
    f.write(config)
    f.close()
