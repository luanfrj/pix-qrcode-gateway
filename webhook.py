#!/usr/bin/python3.7

import requests
import json
import configparser
import psycopg2
import datetime

pix_config = configparser.ConfigParser()
pix_config.read('/home/luanreis/etc/pix-config.ini', encoding='utf-8')
pix_token = pix_config["PIX"]["token"]

database_config = configparser.ConfigParser()
database_config.read('/home/luanreis/etc/database-config.ini', encoding='utf-8')
database_username = database_config["DEFAULT"]["database_username"]
database_password = database_config["DEFAULT"]["database_password"]

def get_con(host, database):
    con = psycopg2.connect(host=host, database=database, user=database_username, password=database_password)
    return con

def get_all_data():
    con = get_con("localhost", "luanreis_afiliate_data")
    cur = con.cursor()
    sql = "SELECT * FROM order_data;"
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    result_set = [dict((cur.description[i][0], value) \
        for i, value in enumerate(row)) for row in rows]
    return result_set

def get_data(id):
    con = get_con("localhost", "luanreis_afiliate_data")
    cur = con.cursor()
    sql = "SELECT * FROM order_data WHERE external_id = " + id + ";"
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()

    if len(rows) < 1:
        return 0
    else:
        result_set = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in rows]
        return result_set
    

def save_data(external_id, status, last_update):
    con = get_con("localhost", "luanreis_afiliate_data")
    cur = con.cursor()
    insert_string = "INSERT INTO order_data (external_id, status, last_update) "
    values_string = "VALUES (" + external_id + ", " + str(status) + ", TIMESTAMP '" + last_update + "');" 
    cur.execute(insert_string + values_string)
    con.commit()
    con.close()

def update_data(external_id, status, last_update):
    con = get_con("localhost", "luanreis_afiliate_data")
    cur = con.cursor()
    sql = ("UPDATE order_data " +
        "SET" +
        " status = " + str(status) + "," 
        " last_update = TIMESTAMP '" + last_update + "'" +
        " WHERE external_id = " + external_id + ";")
    cur.execute(sql)
    con.commit()
    con.close()

def verifiy_order(url):
    headers = {
        "Authorization": "Bearer " + pix_token
    }
    r = requests.get(url, headers=headers)
    order_json = r.text

    order = json.loads(order_json)

    last_update = datetime.datetime.fromisoformat(order["last_updated"])
    status = 0
    if (order["status"] == "closed") and (len(order["payments"]) > 0) and (order["payments"][0]["status"] == "approved"):
        status = 1
    else:
        status = 0

    if get_data(order["external_reference"]) == 0:
        save_data(order["external_reference"], status, last_update.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        update_data(order["external_reference"], status, last_update.strftime("%Y-%m-%d %H:%M:%S"))

def get_all_orders():
    r = get_all_data()
    return json.dumps(r, indent=4, default=str)

def get_order(id):
    r = get_data(id)
    return json.dumps(r, indent=4, default=str)

def get_order_status(id):
    r = get_data(id)
    return str(r[0]["status"])

def receive_webhook(data_json):
    f = open("/home/luanreis/public_html/pix/wbhk.json", "w")
    f.write(json.dumps(data_json, indent=2))
    f.close()
    data = data_json

    if "resource" in data.keys():
        url = data["resource"]
        verifiy_order(url)
    return 0

