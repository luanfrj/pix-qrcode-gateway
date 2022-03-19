#!/usr/bin/python3.7

import create_qrcode
import webhook

from flask import Flask, request, Response, __version__
app = Flask(__name__)
application = app

@app.errorhandler(Exception)
def handle_exception(e):
  f = open("/home/luanreis/public_html/pix/log.txt", "w")
  f.write(str(e))
  f.close()
  return str(e)

@app.route("/qrcode/")
def qrcode():
  id = request.args.get('id', default=0, type=int)
  value = request.args.get('value', default=0.45, type=float)
  response = app.response_class(
    response=create_qrcode.get_qrcode(id, value),
    status=200,
    mimetype='text/plain'
  )
  return response

@app.route("/teste")
def teste():
  response = app.response_class(
    response="00020101021226940014BR.GOV.BCB.PIX2572pix-qr.mercadopago.com/instore/o/v2/73055cb8-ceb7-4c9a-8328-298b0630c6c85204000053039865802BR5904Luan6009SAO PAULO62070503***63042300",
    status=200,
    mimetype='text/plain'
  )
  return response

@app.route("/webhook/", methods=['POST'])
def process_webhook():
  data = request.get_json()
  webhook.receive_webhook(data)
  return Response(status=200)

@app.route("/orders/")
def get_orders():
  response = app.response_class(
    response=webhook.get_all_orders(),
    status=200,
    mimetype='application/json'
  )
  return response

@app.route("/orders/<id>")
def get_order(id):
  response = app.response_class(
    response=webhook.get_order(id),
    status=200,
    mimetype='application/json'
  )
  return response

@app.route("/orders/<id>/status")
def get_order_status(id):
  response = app.response_class(
    response=webhook.get_order_status(id),
    status=200,
    mimetype='text/plain'
  )
  return response

if __name__ == "__main__":
  app.run()