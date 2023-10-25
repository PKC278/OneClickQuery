import base64
import urllib
import requests
import json

API_KEY = ""
SECRET_KEY = ""


class BaiduOCR:
    def main(img):
        url = (
            "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token="
            + BaiduOCR.get_access_token()
        )

        payload = f"image={img}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # 解析JSON字符串
        result_dict = json.loads(response.text)

        # 提取所有words值
        words_list = [item["words"] for item in result_dict["words_result"]]

        # 将所有words值放在一个字符串中
        words_str = " ".join(words_list)

        return words_str

    def get_file_content_as_base64(path, urlencoded=True):
        """
        获取文件base64编码
        :param path: 文件路径
        :param urlencoded: 是否对结果进行urlencoded
        :return: base64编码信息
        """
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf8")
            if urlencoded:
                content = urllib.parse.quote_plus(content)
        return content

    def get_access_token():
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": API_KEY,
            "client_secret": SECRET_KEY,
        }
        return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == "__main__":
    img = BaiduOCR.get_file_content_as_base64("a.png")
    result = BaiduOCR.main(img)
    print(result)
