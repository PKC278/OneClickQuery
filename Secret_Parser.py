import os


def replace_keys_in_file(filename, replacements):
    with open(filename, "r", encoding="utf-8") as f:
        config = f.read()

    for old, new in replacements.items():
        config = config.replace(old, new)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(config)


api_key = os.environ.get("API_KEY")
baiduocr_api_key = os.environ.get("BAIDUOCR_API_KEY")
baiduocr_secret_key = os.environ.get("BAIDUOCR_SECRET_KEY")
tk_token = os.environ.get("TK_TOKEN")

replace_keys_in_file(
    "main/main.py",
    {
        'api_key = ""': f'api_key = "{api_key}"',
        'tk_token = ""': f'tk_token = "{tk_token}"',
    },
)

replace_keys_in_file(
    "main/BaiduOCR.py",
    {
        'API_KEY = ""': f'API_KEY = "{baiduocr_api_key}"',
        'SECRET_KEY = ""': f'SECRET_KEY = "{baiduocr_secret_key}"',
    },
)
