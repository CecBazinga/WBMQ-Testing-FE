import random
import socket
import threading
import time

import requests
from flask import Flask, request, jsonify
from requests import get

botSensorNumber = 50
remoteaddr = 'wbmqsystemproject-dev.us-east-2.elasticbeanstalk.com'

# Data struct to handle random spawn
topics = ['Humidity','Motion','Temperature']
sectors = ['A1','A2','B1','B2','B3','C1','C2','D1','D2','D3']


times_bot =    [0  ,    1,   5,   60]
prob_bot  =    [0.1, 0.69, 0.2, 0.01]

times_sensor = [0  ,    1,   5,   60]
prob_sensor  = [0.1, 0.69, 0.2, 0.01]


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]



#logica di sottoscrizione dei threads
def bot_task_Background( th_data):
    # Richiedo la sub
    data = {}
    if 'id' in th_data:
        data['id'] = th_data['id']
    else:
        data['id'] = ""

    data['current_sector'] = th_data['sector']
    data['topic'] = th_data['topic']
    data['ipaddr'] = ip
    # gfaccio request e ricevo ACK dal broker
    r = requests.post('http://' + remoteaddr + '/bot', json=data)



#logica di gestione dei bot con i threads
def bot_listening_publish():
    app = Flask(__name__)

    @app.route("/", methods=['POST'])
    def wait_for_message():
        sleep_simulation = random.choices(times_bot, prob_bot)
        time.sleep(sleep_simulation[0])

        data = request.get_json()
        msg = data.get('msg', '')
        botId = data.get('botId', '')
        bot_cs = data.get('bot_cs', '')
        sensor = data.get('sensor', '')
        sensor_cs = data.get('sensor_cs', '')
        topic = data.get('topic', '')

        print(botId + " " + bot_cs + " " + sensor + " " + sensor_cs + " " + topic)

        data = {'id': botId, 'message': msg}
        return jsonify(data)

    app.run(debug=True, use_reloader=False, host=get_ip_address(), port=5001)



#logica dei thread publishers
def runBackground(th_data):
    first_request = True
    final_id = ""

    data = {}
    data['current_sector'] = th_data['sector']
    data['type'] = th_data['topic']
    ack = ""
    while True:

        sleep_simulation = random.choices(times_sensor, prob_sensor)
        time.sleep(sleep_simulation[0])

        data['msg'] = str(round(random.uniform(25.5, 50.9), 4))
        data['pbrtx'] = False

        data['id'] = final_id

        try:
            # Happy scenario

            r = requests.post('http://' + remoteaddr + '/sensor', json=data, timeout=5)
            if final_id == "":
                final_id = r.json()['id']
            ack = r.json()['msg']


        except requests.exceptions.ConnectionError:
            print("Pub: Error requesting backend!")

        except requests.exceptions.Timeout:

            while ack != "Ack on message : " + data['msg'] + " on sensorn :" + final_id:

                try:
                    data['pbrtx'] = True
                    r = requests.post('http://' + remoteaddr + '/sensor', json=data, timeout=5)
                    if final_id == "":
                        final_id = r.json()['id']

                    ack = r.json()['msg']

                except requests.exceptions.ConnectionError:
                    print("Pub: Error requesting backend!")

                except requests.exceptions.Timeout:
                    continue





#sottoscrivo i bot
ip = get('https://api.ipify.org').text
for i in range (botSensorNumber):

    sector = random.choice(sectors)
    topic = random.choice(topics)
    th_data={}
    th_data['sector'] = sector
    th_data['topic'] = topic
    maincal = threading.Thread(target=bot_task_Background, args=(th_data,))
    maincal.start()



#spawn di un numero di thread pari al numero di bots per rispondere alle publish del broker
for i in range (botSensorNumber):

    maincal = threading.Thread(target=bot_listening_publish)
    maincal.start()



#spawna i publisher e le requesst
for i in range (botSensorNumber):

    sector = random.choice(sectors)
    topic = random.choice(topics)
    th_data = {}
    th_data['sector'] = sector
    th_data['topic'] = topic
    maincal = threading.Thread(target=runBackground, args=(th_data,))
    maincal.start()
