from flask import Flask, jsonify
import time
import base64
import hashlib
import hmac
import json
import requests

app = Flask(__name__)  # ✅ Flask 앱 선언

API_KEY = 'ff8d0b4a-fdda-4de1-a579-b2076593b7fa'
SECRET_KEY = '49E886BC5608EAB889274AB16323A1B1'
PASSPHRASE = '#eseoAI0612'

def generate_signature(timestamp, method, request_path, body):
    message = f'{timestamp}{method}{request_path}{body}'
    mac = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()

@app.route('/api/balance', methods=['GET'])
def get_balance():
    url = 'https://www.okx.com/api/v5/account/balance'
    timestamp = str(time.time())
    method = 'GET'
    request_path = '/api/v5/account/balance'
    body = ''

    headers = {
        'OK-ACCESS-KEY': API_KEY,
        'OK-ACCESS-SIGN': generate_signature(timestamp, method, request_path, body),
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': PASSPHRASE,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({
            "error": "❌ OKX 호출 실패",
            "exception": str(e)
        }), 500

handler = app  # ✅ Vercel에서 Flask 실행을 위한 엔트리포인트
