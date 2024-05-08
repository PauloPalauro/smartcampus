# smartcampus

O projeto OpenDataTelemetry Stack é centrado em um conjunto de serviços de gateway conectados a Brokers Apache Kafka que distribuem um fluxo de dados em tempo real publicando em um Broker MQTT para mensagens instantâneas e uma API de séries temporais para recuperar dados históricos de um banco de dados InfluxDB.
<br>
<br>
<h2>Funcionamento: </h2>

Um arquivo docker é iniciado com os seguintes processos nele, <b>mosquitto</b>, <b>zookeeper</b>, <b>kafka</b>, <b>telegraf-kafka-mqtt</b> e <b>telegraf-kafka-influxdb</b>. Após isso, executar os dois arquivos Golang para enviar os dados sintenticos para o InfluxDB. <br> <br>
Com a criação da API em Flask, usar os end-points disponivel para pegar os dados do influxDB.
<br>
<br>
End-Points:

- /api/data/WaterTankLavel/{nodename}
- /api/data/Hidrometer/{nodename}
<br>

Trocar os <b>"{nodename}"</b>, pelo nomes dos sensores; <br>
<br>
Os sensores do <b>"WaterTankLavel"</b> são <b>"WaterTankLavel_1"</b> a <b>"WaterTankLavel_8"</b>
<br>
Os sensores do <b>"Hidrometer"</b> são <b>"Hidrometer_1"</b> a <b>"Hidrometer_8"</b>
<br>
<br>
Exemplo com <b>"WaterTankLavel"</b>:
```bash
/api/data/WaterTankLavel/WaterTankLavel_5
```
<br>
Exemplo com <b>"Hidrometer"</b>: 

```bash
 /api/data/WaterTankLavel/Hidrometer_7
```

<br>
<h4>Exemplo de Funcionamento:</h4>
<img src="https://i.imgur.com/CFAVJXX.png" width="" alt="maua monitoria" />
- Obs: Não tenho certeza disso, é como eu acho que funciona pelo que eu fui vendo e mexendo.
<br>
<br>

<h1>Rodar tudo após instalado</h1>
Para instalar tudo certinho e configurado siga o exemplo do repositorio original: <br>
https://github.com/OpenDataTelemetry/OpenDataTelemetry

<br>
<br>
Docker

```bash
cd ~/Git/OpenDataTelemetry/OpenDataTelemetry
sudo docker-compose up
```
<br>
gateway-mqtt-lns-imt with local decoded and simulator

```bash
cd gateway-mqtt-lns-imt
go mod tidy
go run local/main.go
go run simulator/main.go
```
<br>







