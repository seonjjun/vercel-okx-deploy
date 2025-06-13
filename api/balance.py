import time
import base64
import hashlib
import hmac
import json
import requests

API_KEY = '여기에_본인_API_KEY'
SECRET_KEY = '여기에_본인_SECRET_KEY'
PASSPHRASE = '여기에_본인_PASSPHRASE'

def generate_signature(timestamp, method, request_path, body):
    message = f'{timestamp}{method}{request_path}{body}'
    mac = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()

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

    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {
            "error": "❌ OKX 호출 실패",
            "status_code": response.status_code,
            "text": response.text,
            "exception": str(e)
        }

def handler(request):
    return get_balance()
