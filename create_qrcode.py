#!/usr/bin/python3.7

import json
import requests
import datetime
import configparser

pix_config = configparser.ConfigParser()
pix_config.read('~/etc/pix-config.ini', encoding='utf-8')
pix_token = pix_config["PIX"]["token"]
pix_webhook_host = pix_config["PIX"]["webhook_host"]

def gerar_data_hora():
  now = datetime.datetime.now()
  
  expiration = now + datetime.timedelta(minutes=5)
  diferenca = datetime.timedelta(hours=-3)
  fuso_horario = datetime.timezone(diferenca)
  expiration = expiration.astimezone(fuso_horario)

  return expiration.isoformat(sep='T', timespec='milliseconds')


def create_order(external_id, value = 0.25):
  
  order_data = {
    "external_reference": str(external_id),
    "title": "Compra pix teste",
    "description": "Compra pix teste",
    "notification_url": "https://" + pix_webhook_host + "/pix/webhook/",
    "expiration_date": gerar_data_hora(),
    "total_amount": value,
    "items": [
      {
        "title": "Item de teste",
        "description": "Item de teste",
        "unit_price": value,
        "quantity": 1,
        "unit_measure": "unit",
        "total_amount": value
      }
    ]
  }

  url = "https://api.mercadopago.com/instore/orders/qr/seller/collectors/42101078/pos/CAIXA0001/qrs"
  headers = {
    "Authorization": "Bearer " + pix_token,
    "Content-Type": "application/json"
  }

  r = requests.post(url, json=order_data, headers=headers)
  return r.text

def get_qrcode(id, value):
  result_json = create_order(id, value)
  result = json.loads(result_json)
  return result["qr_data"]

