import pytz
from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient
from flask_cors import CORS

# Código em Python usando o framework Flask para criar uma API que consulta dados armazenados em um banco de dados InfluxDB;


app = Flask(__name__) # Cria uma instância do Flask;
CORS(app)  # Configura o CORS para permitir requisições cross-origin;


# Configurações do InfluxDB;
bucket = "smartcampusmaua"
org = "4e336945c11275a9"
token = "Dmd7pZotErhWPDkf0mJEyVffDVJAAmFreaf3xfM7edm-gt12xXdlcxGv8E8MUrSK31o4zLxQK-OALLK9iwKoQg=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com/"
client = InfluxDBClient(url=url, token=token, org=org)

# Define um End-Point da API para recuperar dados do sensor WaterTankLavel com base no seu nome;
@app.route('/api/data/WaterTankLavel/<nodename>', methods=['GET'])
def get_WaterTankLavel_by_nodename(nodename):
    # Query InfluxDB para recuperar dados do hidrômetro com base no nome --> https://docs.influxdata.com/influxdb/v2/query-data/flux/;
    query = f'''
        from(bucket:"{bucket}") 
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "WaterTankLavel")
            |> filter(fn: (r) => r.nodeName == "{nodename}")
            |> filter(fn: (r) => r._field == "data_boardVoltage" or r._field == "data_counter" or r._field == "data_distance" or r._field == "data_humidity" or r._field == "data_temperature")
    '''
    # "client.query_api()" para obter uma instância da API de consulta do InfluxDB.  "query(query)" para enviar a consulta "query" ao banco de dados e receber os resultados. O resultado da consulta é armazenado na variável "result".
    result = client.query_api().query(query)

    # inicializando um dicionário chamado data que será usado para armazenar os dados recuperados da consulta ao banco de dados
    data = {'nodeName': nodename, 'time': [], 'data_boardVoltage': [], 'data_counter': [], 'data_distance': [], 'data_humidity': [], 'data_temperature': []}

    # Iteramos sobre os resultados da consulta (result). Retornar múltiplas tabelas de resultados, estamos percorrendo cada tabela (table) e, em seguida, iterando sobre os registros (record) dentro de cada tabela.
    for table in result:
        for record in table.records:
            time = record.get_time().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S') # convertemos este tempo para o fuso horário de São Paulo
            data['time'].append(time)
            field = record.get_field() # Obtém o nome do campo
            value = record.get_value() # Obtém o valor do campo
            data[field].append(value)
    return jsonify(data)  # Retorna os dados em formato JSON 


# Mesmo processo acima só que com hidrometer
@app.route('/api/data/Hidrometer/<nodename>', methods=['GET'])
def get_Hidrometer_by_nodename(nodename):
    query = f'''
        from(bucket:"{bucket}")
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "Hidrometer")
            |> filter(fn: (r) => r.nodeName == "{nodename}")
            |> filter(fn: (r) => r._field == "data_boardVoltage" or r._field == "data_counter")
    '''
    result = client.query_api().query(query)
    data = {'nodeName': nodename,'time': [], 'data_boardVoltage': [], 'data_counter': []}
    for table in result:
        for record in table.records:
            time = record.get_time().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
            data['time'].append(time)
            field = record.get_field()
            value = record.get_value()
            data[field].append(value)
    return jsonify(data)


@app.route('/api/data/ArtesianWell', methods=['GET'])
def get_ArtesianWell():
    query = f'''
        from(bucket:"{bucket}")
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "ArtesianWell")
            |> filter(fn: (r) => r.nodeName == "ArtesianWell_1")
            |> filter(fn: (r) => r._field == "data_boardVoltage" or r._field == "data_pressure_0" or r._field == "data_pressure_1")
    '''
    result = client.query_api().query(query)
    data = {'nodeName': "ArtesianWell_1", 'time': [], 'data_boardVoltage': [], 'data_pressure_0': [], 'data_pressure_1': []}
    for table in result:
        for record in table.records:
            time = record.get_time().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
            data['time'].append(time)
            field = record.get_field()
            value = record.get_value()
            data[field].append(value)
    return jsonify(data)


# Inicia o servidor Flask em modo de depuração
if __name__ == '__main__':
    app.run(debug=True)
