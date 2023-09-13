import requests
import json
import os
import requests
import json

def image_generate(content):
    # 定义图像生成的API端点
    api_endpoint = "http://localhost:8080/v1/images/generations"
    api_key="key-1234567890"
    # 创建一个JSON payload，包含内容
    payload = {
        "prompt": content,
        "size": "256x256"  # 可根据需要调整图像大小
    }

    try:
        # 发送POST请求到API
        response = requests.post(api_endpoint, json=payload, headers={"Content-Type": "application/json"})

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析响应JSON以获取生成的图像URL
            result = response.json()
            generated_image_url = result['data'][0]['url']

            return generated_image_url
        else:
            # 处理API请求错误
            return None

    except Exception as e:
        # 处理任何异常
        return None