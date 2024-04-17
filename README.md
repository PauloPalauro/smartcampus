# smartcampus

O projeto OpenDataTelemetry Stack é centrado em um conjunto de serviços de gateway conectados a Brokers Apache Kafka que distribuem um fluxo de dados em tempo real publicando em um Broker MQTT para mensagens instantâneas e uma API de séries temporais para recuperar dados históricos de um banco de dados InfluxDB.
<br>
<br>
<h2>Ambiente de Desenvolvimento: </h2>

O ambiente de desenvolvimento consiste em um arquivo docker-compose.yaml que configura um Broker MQTT sem senha necessária, um Broker Apache Kafka e arquivos de configuração do Telegraf.
Dois arquivos de configuração do Telegraf estão presentes: um conecta-se ao Broker Kafka e escreve no InfluxDB, enquanto o outro publica em um Broker MQTT.
<br>
<br>
<h2> Atividades do Desenvolvedor:</h2>

O desenvolvedor deve se concentrar em estabelecer uma conexão com a origem dos dados, decodificá-los e enviá-los para o Broker Kafka com as entradas dos gateways.
Além disso, o desenvolvedor deve gerar soluções para trabalhar com os dados decodificados em tempo real e analisá-los usando um serviço de assinatura MQTT e as saídas da API de séries temporais.
<br>
<br>
<h2>Configuração e Execução do Ambiente:</h2>

O desenvolvedor é instruído a baixar o repositório, configurar e executar os Brokers e os arquivos Telegraf para escrever em um banco de dados InfluxDB hospedado na nuvem.
Instruções detalhadas sobre a configuração e execução dos componentes do ambiente estão fornecidas no README.
<br>
<br>
<h2>Gateways e Decodificação:</h2>

O gateway é onde os dados são recebidos, decodificados e enviados para o Broker Apache Kafka.
É fornecido um exemplo específico de um gateway chamado gateway-mqtt-lns-imt que se conecta ao Servidor de Rede Lora (LNS) do Instituto Maua de Tecnologia (IMT) via Broker MQTT.
<br>
<br>
<h2>Simulação de Dados Sintéticos:</h2>

Um simulador de dados sintéticos é fornecido para simular a geração de dados de sensores e publicá-los no Broker MQTT local.
<br>
<br>
<h2>API de Séries Temporais:</h2>

A API de séries temporais é responsável por recuperar dados do InfluxDB Cloud, especificamente disponível para alguns endpoints SmartLight.
<br>
<br>
<h2>Instruções de Configuração e Execução da API de Séries Temporais:</h2>

O README fornece instruções sobre como clonar, configurar e executar a API de séries temporais, incluindo a configuração das variáveis de ambiente necessárias.
Essas são as etapas principais e os pontos-chave que o README do projeto OpenDataTelemetry aborda. 

<br>
<br>
<h1>Rodar tudo após instalado</h1>
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

Run timeseries-api

```bash
cd timeseries-api
go mod tidy

INFLUXDB_URL=https://us-east-1-1.aws.cloud2.influxdata.com \
  INFLUXDB_DATABASE=smartcampusmaua \
  INFLUXDB_TOKEN="INFLUX_READ_TOKEN_HERE" go run main.go
```
<br>

Subscribe to a Topic and listen for simulator data at MQTT

```bash
mosquitto_sub -h localhost -t "application/+/node/+/rx"
```
<br>

Subscribe to a Topic and listen for decoded JSON data at MQTT:

```bash
mosquitto_sub -h localhost -t "SmartCampusMaua/#"
```
<br>

<h1>Duvidas</h1>
<h3>Para que o docker serve nesse projeto?</h3>
<br>
<b>R:</b> O arquivo docker-compose.yaml neste projeto serve para definir e gerenciar os serviços necessários para o ambiente de desenvolvimento do OpenDataTelemetry. 
<br>
- mosquitto <br>
- zookeeper <br>
- kafka <br>
- telegraf-kafka-influxdb <br>
- telegraf-kafka-mqtt <br>
<br>
Esses serviços trabalham juntos para criar um ambiente de desenvolvimento funcional para o projeto OpenDataTelemetry, permitindo que os desenvolvedores testem e trabalhem com os diferentes componentes do sistema, como MQTT, Kafka e InfluxDB
<br>
<br>
<br>
<h3>O que é o "go run simulator/main.go" quando executado?</h3> <br>
<b>R:</b> o programa está simulando o envio de dados para o broker MQTT em intervalos regulares. As linhas que começam com "t:" são os registros de tempo (em nanossegundos desde o Unix epoch) nos quais os dados foram enviados para o broker MQTT. <br>
Cada linha "t:" indica um momento específico em que os dados foram gerados e publicados no broker MQTT. Esses registros de tempo podem ser úteis para rastrear e analisar o momento em que os dados foram enviados durante a simulação.
<br>
<br>
<br>
<h3>Com o "go run simulator/main.go" executado, o "o go run local/main.go" começa a dar respostas, o que são?</h3> <br>
<b>R:</b> Quando você executa go run local/main.go após iniciar o simulador com go run simulator/main.go, o programa local/main.go começa a receber os dados simulados do sensor e os processa.<br>
Além disso, os outros dados na saída fornecem informações sobre os metadados associados aos dados recebidos, como o nome do aplicativo, o ID do aplicativo, o EUI do dispositivo, informações de transmissão, informações de recepção, etc. Essas informações são úteis para entender o contexto em que os dados foram gerados e entregues.
<br>
<br>
<br>
<h3>O que é o time series API?</h3> <br>
<b>R:</b> A parte do timeseries-api é necessária para acessar e recuperar os dados armazenados no banco de dados InfluxDB Cloud. Este banco de dados está sendo usado para armazenar os dados coletados dos dispositivos, como os sensores simulados SmartLight, WaterTankLevel e Hidrometer.
<br>
O timeseries-api é responsável por fazer consultas ao banco de dados InfluxDB Cloud e recuperar os dados históricos armazenados lá. Isso pode ser útil para análises de dados, visualizações ou qualquer outro tipo de processamento que você deseje realizar com os dados coletados.
<br>
<br>
<br>
<h3>O que é o comando "mosquitto_sub -h localhost -t "application/+/node/+/rx""?</h3> <br>
<b>R:</b> Este comando se inscreve em um tópico MQTT específico para ouvir os dados simulados que estão sendo enviados. O tópico é definido como "application/+/node/+/rx", o que significa que ele vai corresponder a qualquer mensagem publicada em um tópico que comece com "application/", seguido por qualquer valor, então "/node/", outro valor, e "/rx" no final. Isso pode ser usado para ouvir os dados dos dispositivos simulados.
<br>
<br>
<br>
<h3>O que é o comando "mosquitto_sub -h localhost -t "SmartCampusMaua/#""?</h3> <br>
<b>R:</b> Este comando se inscreve em um tópico MQTT específico para ouvir os dados JSON decodificados que estão sendo publicados. O tópico é definido como "SmartCampusMaua/#", o que significa que ele vai corresponder a qualquer mensagem publicada em qualquer sub-tópico de "SmartCampusMaua/". Isso pode ser usado para ouvir os dados decodificados dos dispositivos.










