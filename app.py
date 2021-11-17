import json
import config
from flask import Flask, request, jsonify
from binance.client import Client
from binance.enums import *


app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET) #, tld='us'

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} - {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": 'Lỗi cmnr',
            "message": 'Cố gắng lần sau nhé, sai mật khẩu'
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    order_response = order(side, quantity, "BNBUSDT")
    print(side)
    print(quantity)
    print(order_response)

    if order_response:
        return {
            "code": 'Nhập liệu thành công',
            'message': 'order excuted'
        }
    else:
        print('order failed')
        return {
            'code': 'error',
            'message': 'order failed'
        }

# Câu lệnh tạo app
# export FLASK_APP=app.py
# flask run

# Để máy tự cập nhật liên tục theo file py thì nhập
# export FLASK_ENV=development
# flask run