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


@app.route('/api/data/WaterTankLavel', methods=['GET'])
def get_WaterTankLavel():
    data_by_nodename = {}
    for nodename in range(1, 9):  
        query = f'''
            from(bucket:"{bucket}") 
                |> range(start: -1h)
                |> filter(fn: (r) => r._measurement == "WaterTankLavel")
                |> filter(fn: (r) => r.nodeName == "WaterTankLavel_{nodename}")
                |> filter(fn: (r) => r._field == "data_distance")
        '''
        result = client.query_api().query(query)
        nodename_data = {'data_distance': [], 'timestamp': []}

        for table in result:
            for record in table.records:
                time = record.get_time().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
                nodename_data['timestamp'].append(time)
                value = record.get_value()
                nodename_data['data_distance'].append(value)
        data_by_nodename[f'WaterTankLavel_{nodename}'] = nodename_data

    return jsonify(data_by_nodename)




@app.route('/api/data/Hidrometer', methods=['GET'])
def get_Hidrometer():
    data_by_nodename = {}
    for nodename in range(1, 9):  
        query = f'''
            from(bucket:"{bucket}") 
                |> range(start: -1h)
                |> filter(fn: (r) => r._measurement == "Hidrometer")
                |> filter(fn: (r) => r.nodeName == "Hidrometer_{nodename}")
                |> filter(fn: (r) => r._field == "data_counter")
        '''
        result = client.query_api().query(query)
        nodename_data = {'data_counter': [], 'timestamp': []}

        for table in result:
            for record in table.records:
                time = record.get_time().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
                nodename_data['timestamp'].append(time)
                value = record.get_value()
                nodename_data['data_counter'].append(value)
        data_by_nodename[f'Hidrometer_{nodename}'] = nodename_data
    return jsonify(data_by_nodename)




@app.route('/api/data/ArtesianWell', methods=['GET'])
def get_ArtesianWell():
    query = f'''
        from(bucket:"{bucket}")
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "ArtesianWell")
            |> filter(fn: (r) => r.nodeName == "ArtesianWell_1")
            |> filter(fn: (r) => r._field == "data_pressure_0" or r._field == "data_pressure_1")
    '''
    result = client.query_api().query(query)
    data = {'data_pressure_0': [], 'data_pressure_1': [], 'timestamp': []}
    for table in result:
        for record in table.records:
            time = record.get_time().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
            data['timestamp'].append(time)
            field = record.get_field()
            value = record.get_value()
            data[field].append(value)
    return jsonify({"ArtesianWell": data})


# Inicia o servidor Flask em modo de depuração
if __name__ == '__main__':
    app.run(debug=True)
