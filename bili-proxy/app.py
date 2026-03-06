import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求，生产环境可更严格配置

# B站官方API地址
BILI_API_URL = "https://api.bilibili.com/x/web-interface/view"

# 模拟浏览器请求头，降低被B站拦截的概率
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com',
    'Origin': 'https://www.bilibili.com'
}

@app.route('/bili/video', methods=['GET'])
def get_video_info():
    """接收bvid参数，返回B站视频数据"""
    bvid = request.args.get('bvid')
    if not bvid:
        return jsonify({'code': -1, 'message': '缺少bvid参数'}), 400

    # 可选：添加简单的请求频率控制（例如每IP每秒最多5次），防止滥用
    # 这里省略，您可以根据需要实现

    try:
        resp = requests.get(
            BILI_API_URL,
            params={'bvid': bvid},
            headers=HEADERS,
            timeout=5  # 设置超时，避免长时间阻塞
        )
        resp.raise_for_status()  # 如果状态码不是200，会抛出异常
        data = resp.json()

        # 直接透传B站的返回结构，前端无需修改解析逻辑
        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({'code': -2, 'message': '请求B站超时'}), 504
    except requests.exceptions.RequestException as e:
        # 打印日志方便调试（生产环境建议使用logging）
        print(f"请求B站失败: {e}")
        return jsonify({'code': -3, 'message': '无法连接到B站'}), 502
    except Exception as e:
        return jsonify({'code': -4, 'message': '服务器内部错误'}), 500

if __name__ == '__main__':
    # 监听所有网络接口，前端可以通过IP访问；调试模式开启方便开发
    app.run(host='0.0.0.0', port=5000, debug=True)