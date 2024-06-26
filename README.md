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

- /api/data/WaterTankLavel
- /api/data/Hidrometer
- /api/data/ArtesianWell
<br>

Exemplo de Resposta (WaterTankLavel): <br>

>{ <br>
   "WaterTankLavel_1": { <br>
    &nbsp; &nbsp; &nbsp;"data_distance": [], <br>
    &nbsp; &nbsp; &nbsp;"timestamp": [] <br>
  &nbsp;}, <br>
  "WaterTankLavel_2": { <br>
     &nbsp; &nbsp; &nbsp;"data_distance": [], <br>
     &nbsp; &nbsp; &nbsp;"timestamp": [] <br>
 &nbsp; }, <br>
}


<br>
<h4>Exemplo de Funcionamento:</h4>
<img src="https://i.imgur.com/CFAVJXX.png" width="" alt="maua monitoria" />
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







