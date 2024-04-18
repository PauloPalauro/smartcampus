import pytz
from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Configurações do InfluxDB
bucket = "smartcampusmaua"
org = "4e336945c11275a9"
token = "Dmd7pZotErhWPDkf0mJEyVffDVJAAmFreaf3xfM7edm-gt12xXdlcxGv8E8MUrSK31o4zLxQK-OALLK9iwKoQg=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com/"
client = InfluxDBClient(url=url, token=token, org=org)

@app.route('/api/data/WaterTankLavel/<nodename>', methods=['GET'])
def get_WaterTankLavel_by_nodename(nodename):
    query = f'''
        from(bucket:"{bucket}")
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "WaterTankLavel")
            |> filter(fn: (r) => r.nodeName == "{nodename}")
            |> filter(fn: (r) => r._field == "data_boardVoltage" or r._field == "data_counter" or r._field == "data_distance" or r._field == "data_humidity" or r._field == "data_temperature")
    '''
    result = client.query_api().query(query)
    data = {'nodeName': nodename, 'time': [], 'data_boardVoltage': [], 'data_counter': [], 'data_distance': [], 'data_humidity': [], 'data_temperature': []}
    for table in result:
        for record in table.records:
            time = record.get_time().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
            data['time'].append(time)
            field = record.get_field()
            value = record.get_value()
            data[field].append(value)
    return jsonify(data)    


@app.route('/api/data/Hidrometer/<nodename>', methods=['GET'])
def get_Hidrometer_by_nodename(nodename):
    query = f'''
        from(bucket:"{bucket}")
            |> range(start: -5h)
            |> filter(fn: (r) => r._measurement == "Hidrometer")
            |> filter(fn: (r) => r.nodeName == "{nodename}")
            |> filter(fn: (r) => r._field == "data_boardVoltage" or r._field == "data_counter" or r._field == "data_humidity" or r._field == "data_temperature")
    '''
    result = client.query_api().query(query)
    data = {'nodeName': nodename,'time': [], 'data_boardVoltage': [], 'data_counter': [], 'data_humidity': [], 'data_temperature': []}
    for table in result:
        for record in table.records:
            time = record.get_time().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
            data['time'].append(time)
            field = record.get_field()
            value = record.get_value()
            data[field].append(value)
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
