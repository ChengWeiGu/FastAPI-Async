import uvicorn
import json
import configparser
from fastapi import FastAPI, Request
import asyncio
import aioodbc
import pandas as pd
import socket

current_ip = socket.gethostbyname(socket.gethostname())

config = configparser.ConfigParser()
config.read('config.ini')

# 讀取資料庫相關設定
driver = config['DB']['driver']
server = config['DB']['server']
database = config['DB']['database']
username = config['DB']['username']
password = config['DB']['password']

app = FastAPI()

# define a operation like the select query
async def perform_async_query(accound_id):
    tablename = '[WEC_AUTO_FR].[dbo].[openai_api_cost]'
    columns = '[accound_id],sum([cost]) as accumulated_cost'
    additional = 'group by [accound_id]'
    where_condition = f"accound_id = '{accound_id}'"
    strSQL = f"SELECT {columns} FROM {tablename} WHERE {where_condition} {additional}"
    conn_str = "DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (driver,server,database,username,password)
    data = []
    async with aioodbc.connect(dsn=conn_str) as conn:
        cursor = await conn.cursor()
        await cursor.execute(strSQL)
        rows = await cursor.fetchall()
        for row in rows:
            _accound_id = row[0]
            _accumulated_cost = row[1]
            data += [{'accound_id':_accound_id,'accumulated_cost':_accumulated_cost}]
            # print(row)
        await cursor.close()
    df = pd.DataFrame(data)
    return df



'''
1. For fastapi, we use @app.post(/your_path). For flask, we use @app.route(/your_path)
2. we add key word "async" before def
3. we input the parameter (request:Request) in the fun
4. Note that key word "await" should be added before request.body()
''' 
# Home Page
@app.get("/home")
async def get_home(request:Request):
    # url
    request_url = request.url._url
    # receive data from request
    data = await request.body()
    json_data = data.decode('utf-8')
    json_data = json.loads(json_data)
    # return a json
    resp_msg = "Hellow Wrold"
    resp_json = {"request_url":request_url,
                "request_data":json_data,
                "resp_msg":resp_msg}
    return resp_json


# get_quota
@app.post("/get_quota")
async def get_quota(request:Request):
    # url
    request_url = request.url._url
    # receive data from request
    data = await request.body()
    json_data = data.decode('utf-8')
    json_data = json.loads(json_data)
    # return a json
    account_id = json_data["account_id"]
    try:
        df_cost = await perform_async_query(account_id)
        resp_json = {"request_url":request_url,
                    "request_data":json_data,
                    "response_data":df_cost,
                    "response_result":"success"}
    except Exception as e:
        resp_json = {"request_url":request_url,
                    "request_data":json_data,
                    "error_reason":str(e),
                    "response_result":"fail"}
    
    return resp_json


if __name__ == "__main__":
   uvicorn.run(app, host=current_ip, port=8080)




