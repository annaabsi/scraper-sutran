import datetime
import pandas as pd
import requests
import io
import json

url = 'http://gis.sutran.gob.pe/alerta_sutran/script_cgm/carga_xlsx.php'
headers = {'Accept': '/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en,es;q=0.9,en-GB;q=0.8',
'Connection': 'keep-alive',
'Content-Length': '9',
'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8-SIG',
'Host': 'gis.sutran.gob.pe',
'Origin': 'http://gis.sutran.gob.pe',
'Referer': 'http://gis.sutran.gob.pe/alerta_sutran/',
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'}
body = {'tipo':'MAPA'}
req = requests.post(url, headers=headers, data=body)
now = datetime.datetime.now()

my_json = json.load(io.BytesIO(req.content))

restringido = {}
restringido['data'] = my_json['restringido']

interrumpido = {}
interrumpido['data'] = my_json['interrumpido']

with open('restringido.json', 'w') as f:
    json.dump(restringido, f)

with open('interrumpido.json', 'w') as f:
    json.dump(interrumpido, f)

df_r = pd.read_json('restringido.json', encoding = 'utf-8-sig', orient='split')
df_restringido = pd.json_normalize(df_r['properties'])

df_i = pd.read_json('interrumpido.json', encoding = 'utf-8-sig', orient='split')
df_interrumpido = pd.json_normalize(df_i['properties'])

frames = [df_restringido, df_interrumpido]
df_total = pd.concat(frames, ignore_index=True)
df_total = df_total[df_total['motivo'] == 'HUMANO']
df_total = df_total.replace('TRANSITO', 'TRÁNSITO', regex=True)
df_total = df_total.replace('"', '', regex=True)
df_total['style'] = df_total['estado'].str.split(' ').str[1].str.lower()
df_total.to_csv(f'resultados/flourish.csv', index=False)