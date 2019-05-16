import paho.mqtt.client as mqtt
import schedule
import time
import datetime
import json
import sys
import string
import random
import GSM as gsm
from pprint import pprint

topic = {
        "settings" : "bscpe_topics_hives/settings",
        "live_reports" : "bscpe_topics_hives/reports/live",
        "history" : "bscpe_topics_hives/reports/history",
        "alerts" : "bscpe_topics_hives/alerts",
        "numbers": "bscpe_topics_hives/numbers",
        
        }

broker = {
        "eclipse":"broker.hivemq.com",
        "mosquitto":"test.mosquitto.org"
        }
directory = {
            "log":'/home/pi/BeeHiveMonitoring/log.json',
            "history":'/home/pi/BeeHiveMonitoring/history.json',
            "parameters":'/home/pi/BeeHiveMonitoring/Parameters.json',
            "numbers":'/home/pi/BeeHiveMonitoring/Numbers.json',
            "initialWeights":'/home/pi/BeeHiveMonitoring/InitialWeights.json'
            }

   


def idGenerator(size = 25, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def scheduler():
    schedule.clear()
    #get weight report interval
    with open(directory["parameters"],'r') as f:
            params = json.load(f)
            interval = params['Parameters']['Time_Span']
    #start scheduling
    if(interval > 1):
        schedule.every(interval).days.at("08:00").do(Hive_weight_reporting)
    else:
        schedule.every().day.at("08:00").do(Hive_weight_reporting)
    schedule.every(10).minutes.do(healthCheck)
    #schedule.every(60).seconds.do(Hive_weight_reporting)
    schedule.every(5).seconds.do(reportLog)
    schedule.every().day.at("08:00").do(reportHistory)
    print()
    print(schedule.jobs)
    print()     
    print("Successful")
    
def on_connect(client, obj, flags, rc):
    
    if(str(rc) == "0"):
        print("RC: 0 MQTT Connection successful")      
        
    if(rc == 1):
        error = "RC: 1 MQTT Connection refused - incorrect protocol version"
        print(error)
        gsm.sendSMS(error)
    if(rc == 2):
        error = "RC:2 MQTT Connection refused - invalid client identifier"
        print(error)
        gsm.sendSMS(error)
    if(rc == 3):
        error = "RC:3 MQTT Connection refused - server unavailable"
        print(error)
        gsm.sendSMS(error)
    if(rc == 4):
        error = "RC:5 MQTT Connection refused - bad username or password"
        print(error)
        gsm.sendSMS(error)
    if(rc == 5):
        error = "RC:6 MQTT Connection refused - not authorised"
        print(error)
        gsm.sendSMS(error)
        
def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " ")

    if(msg.topic == topic["settings"]):
        payload = msg.payload.decode('utf-8')
        params = json.loads(payload)
        print("New Parameters Received!")
        print(params["Parameters"])

        with open(directory['parameters'],'w')as out:
            json.dump(params,out,indent=4,sort_keys = True)
    
        print("Saved!")
        print("Applying New Schedule...")
        scheduler()
        
    elif(msg.topic == topic["numbers"]):
        payload = msg.payload.decode('utf-8')
        nums = json.loads(payload)
        with open(directory['numbers'],'w')as out:
            json.dump(nums,out,indent=4,sort_keys = True)
    
def on_publish(client, obj, mid):
    print("sent! mid: " + str(mid))
    pass


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    print(string)
    
ID = idGenerator()
print(ID)
client = mqtt.Client(ID)

client.on_message = on_message
client.on_connect = on_connect

client.connect(broker["eclipse"])
client.subscribe(topic["settings"])
client.subscribe(topic["numbers"])
client.loop_start()


                   
def reportLog():
    log = open(directory["log"],'r')
    jsonData = log.read()    
    client.publish(topic["live_reports"],jsonData,0)
    print("log sent! {0}".format(str(datetime.datetime.now())))
    print("----------------------------------")
    
    
def reportHistory():
    historyLog = open(directory["history"],'r')
    jsonData = historyLog.read()    
    client.publish(topic["history"],jsonData, 0,True)
    print("history sent!")
    print("----------------------------------")

def testTopic():
    while(True):
        try:
            client.publish(topic["live_reports"],"Thid is a test.")
            print("ok")
            time.sleep(1)
        except:
            raise

def healthCheck():
    print("--------------")
    print("Health Check")
    print("--------------")
    directory["parameters"]
    
    with open(directory["parameters"],'r') as f:
        params = json.load(f)
        
    with open(directory["history"],'r') as f:
        history = json.load(f)

    Temp_Anomaly = []
    Humid_Anomaly = []
    
    Max_Temp_layer1 = params['Parameters']['Max_Temp']
    Max_Temp_layer2 = params['Parameters']['Max_Temp2']
    Min_Temp_layer1 = params['Parameters']['Min_Temp']
    Min_Temp_layer2 = params['Parameters']['Min_Temp2']
    Max_Humid_layer1 = params['Parameters']['Max_Humid']
    Max_Humid_layer2 = params['Parameters']['Max_Humid2']
    Min_Humid_layer1 = params['Parameters']['Min_Humid']
    Min_Humid_layer2 = params['Parameters']['Min_Humid2']
    Harvest_Weight = params['Parameters']['Harvest_Weight']
   
    hive1_layer1_temp = history['Reports'][-1]['Hive_1']['Temperatures'][0]
    hive1_layer2_temp = history['Reports'][-1]['Hive_1']['Temperatures'][1]
    
    hive2_layer1_temp = history['Reports'][-1]['Hive_2']['Temperatures'][0]
    hive2_layer2_temp = history['Reports'][-1]['Hive_2']['Temperatures'][1]

    hive3_layer1_temp = history['Reports'][-1]['Hive_3']['Temperatures'][0]
    hive3_layer2_temp = history['Reports'][-1]['Hive_3']['Temperatures'][1]


    hive1_layer1_humid = history['Reports'][-1]['Hive_1']['Humidities'][0]
    hive1_layer2_humid = history['Reports'][-1]['Hive_1']['Humidities'][1]

    hive2_layer1_humid = history['Reports'][-1]['Hive_2']['Humidities'][0]
    hive2_layer2_humid = history['Reports'][-1]['Hive_2']['Humidities'][1]
        
    hive3_layer1_humid = history['Reports'][-1]['Hive_3']['Humidities'][0]
    hive3_layer2_humid = history['Reports'][-1]['Hive_3']['Humidities'][1]
    
    hive1_weight = history['Reports'][-1]['Hive_1']['Weight']
    hive2_weight = history['Reports'][-1]['Hive_2']['Weight']
    hive3_weight = history['Reports'][-1]['Hive_3']['Weight']
    
    

    #Hive 1 layer1 temp Temp_Anomaly
    if(hive1_layer1_temp > Max_Temp_layer1):
        Temp_Anomaly.append("ALERT!!\nHive 1 Layer 1 temperature is at {0:.2f}C, which exceeds {1:.2f}C MAXIMUM temperature set in the app.\nDate&Time: {2}".format(hive1_layer1_temp,Max_Temp_layer1,datetime.datetime.now()))
    elif(hive1_layer1_temp < Min_Temp_layer1):
        Temp_Anomaly.append("ALERT!!\nHive 1 Layer 1 temperature is at {0:.2f}C, which exceeds {1:.2f}C MINIMUM temperature set in the app.\nDate&Time: {2}".format(hive1_layer1_temp,Min_Temp_layer1,datetime.datetime.now()))
    #Hive 1 layer2 temp Temp_Anomaly
    if(hive1_layer2_temp > Max_Temp_layer2):
        Temp_Anomaly.append("ALERT!!\nHive 1 Layer 2 temperature is at {0:.2f}C, which exceeds {1:.2f}C MAXIMUM temperature set in the app.\nDate&Time: {2}".format(hive1_layer2_temp,Max_Temp_layer2,datetime.datetime.now()))
    elif(hive1_layer2_temp < Min_Temp_layer2):
        Temp_Anomaly.append("ALERT!!\nHive 1 Layer 2 temperature is at {0:.2f}C, which exceeds {1:.2f}C MINIMUM temperature set in the app.\nDate&Time: {2}".format(hive1_layer2_temp,Min_Temp_layer2,datetime.datetime.now()))
    
    #Hive 2 layer1 temp Temp_Anomaly
    if(hive2_layer1_temp > Max_Temp_layer1):
        Temp_Anomaly.append("ALERT!!\nHive 2 Layer 1 temperature is at {0:.2f}C, which exceeds {1:.2f}C MAXIMUM temperature set in the app.\nDate&Time: {2}".format(hive2_layer1_temp,Max_Temp_layer1,datetime.datetime.now()))
    elif(hive2_layer1_temp < Min_Temp_layer1):
        Temp_Anomaly.append("ALERT!!\nHive 2 Layer 1 temperature is at {0:.2f}C, which exceeds {1:.2f}C MINIMUM temperature set in the app.\nDate&Time: {2}".format(hive2_layer1_temp,Min_Temp_layer1,datetime.datetime.now()))
    #Hive 2 layer2 temp Temp_Anomaly
    if(hive2_layer2_temp > Max_Temp_layer2):
        Temp_Anomaly.append("ALERT!!\nHive 2 Layer 2 temperature is at {0:.2f}C, which exceeds {1:.2f}C MAXIMUM temperature set in the app.\nDate&Time: {2}".format(hive2_layer2_temp,Max_Temp_layer2,datetime.datetime.now()))
    elif(hive2_layer2_temp < Min_Temp_layer2):
        Temp_Anomaly.append("ALERT!!\nHive 2 Layer 2 temperature is at {0:.2f}C, which exceeds {1:.2f}C MINIMUM temperature set in the app.\nDate&Time: {2}".format(hive2_layer2_temp,Min_Temp_layer2,datetime.datetime.now()))
   

    #Hive 3 layer1 temp Temp_Anomaly
    if(hive3_layer1_temp > Max_Temp_layer1):
        Temp_Anomaly.append("ALERT!!\nHive 3 Layer 1 temperature is at {0:.2f}C, which exceeds {1:.2f}C MAXIMUM temperature set in the app.\nDate&Time: {2}".format(hive3_layer1_temp,Max_Temp_layer1,datetime.datetime.now()))
    elif(hive2_layer1_temp < Min_Temp_layer1):
        Temp_Anomaly.append("ALERT!!\nHive 3 Layer 1 temperature is at {0:.2f}C, which exceeds {1:.2f}C MINIMUM temperature set in the app.\nDate&Time: {2}".format(hive3_layer1_temp,Min_Temp_layer1,datetime.datetime.now()))
    #Hive 2 layer2 temp Temp_Anomaly
    if(hive3_layer2_temp > Max_Temp_layer2):
        Temp_Anomaly.append("ALERT!!\nHive 3 Layer 2 temperature is at {0:.2f}C, which exceeds {1:.2f}C MAXIMUM temperature set in the app.\nDate&Time: {2}".format(hive3_layer2_temp,Max_Temp_layer2,datetime.datetime.now()))
    elif(hive3_layer2_temp < Min_Temp_layer2):
        Temp_Anomaly.append("ALERT!!\nHive 3 Layer 2 temperature is at {0:.2f}C, which exceeds {1:.2f}C MINIMUM temperature set in the app.\nDate&Time: {2}".format(hive3_layer2_temp,Min_Temp_layer2,datetime.datetime.now()))



    #Hive 1 layer1 humid 
    if(hive1_layer1_humid > Max_Humid_layer1):
        Humid_Anomaly.append("ALERT!!\nHive 1 Layer 1 humidity is at {0:.2f}%, which exceeds {1:.2f}% MAXIMUM humidity set in the app.\nDate&Time: {2}".format(hive1_layer1_humid,Max_Humid_layer1,datetime.datetime.now()))
    elif(hive1_layer1_humid < Min_Humid_layer1):
        Humid_Anomaly.append("ALERT!!\nHive 1 Layer 1 humidity is at {0:.2f}%, which exceeds {1:.2f}% MINIMUM humidity set in the app.\nDate&Time: {2}".format(hive1_layer1_humid,Min_Humid_layer1,datetime.datetime.now()))
    #Hive 1 layer2 humid 
    if(hive1_layer2_humid > Max_Humid_layer2):
        Humid_Anomaly.append("ALERT!!\nHive 1 Layer 2 humidity is at {0:.2f}%, which exceeds {1:.2f}% MAXIMUM humidity set in the app.\nDate&Time: {2}".format(hive1_layer2_humid,Max_Humid_layer2,datetime.datetime.now()))
    elif(hive1_layer2_humid < Min_Humid_layer2):
        Humid_Anomaly.append("ALERT!!\nHive 1 Layer 2 humidity is at {0:.2f}%, which exceeds {1:.2f}% MINIMUM humidity set in the app.\nDate&Time: {2}".format(hive1_layer2_humid,Min_Humid_layer2,datetime.datetime.now()))
    
     #Hive 2 layer1 humid 
    if(hive2_layer1_humid > Max_Humid_layer1):
        Humid_Anomaly.append("ALERT!!\nHive 2 Layer 1 humidity is at {0:.2f}%, which exceeds {1:.2f}% MAXIMUM humidity set in the app.\nDate&Time: {2}".format(hive2_layer1_humid,Max_Humid_layer1,datetime.datetime.now()))
    elif(hive2_layer1_humid < Min_Humid_layer1):
        Humid_Anomaly.append("ALERT!!\nHive 2 Layer 1 humidity is at {0:.2f}%, which exceeds {1:.2f}% MINIMUM humidity set in the app.\nDate&Time: {2}".format(hive2_layer1_humid,Min_Humid_layer1,datetime.datetime.now()))
    #Hive 2 layer2 humid 
    if(hive2_layer2_humid > Max_Humid_layer2):
        Humid_Anomaly.append("ALERT!!\nHive 2 Layer 2 humidity is at {0:.2f}%, which exceeds {1:.2f}% MAXIMUM humidity set in the app.\nDate&Time: {2}".format(hive2_layer2_humid,Max_Humid_layer2,datetime.datetime.now()))
    elif(hive2_layer2_humid < Min_Humid_layer2):
        Humid_Anomaly.append("ALERT!!\nHive 2 Layer 2 humidity is at {0:.2f}%, which exceeds {1:.2f}% MINIMUM humidity set in the app.\nDate&Time: {2}".format(hive2_layer2_humid,Min_Humid_layer2,datetime.datetime.now()))
    
     #Hive 3 layer1 humid 
    if(hive3_layer1_humid > Max_Humid_layer1):
        Humid_Anomaly.append("ALERT!!\nHive 3 Layer 1 humidity is at {0:.2f}%, which exceeds {1:.2f}% MAXIMUM humidity set in the app.\nDate&Time: {2}".format(hive3_layer1_humid,Max_Humid_layer1,datetime.datetime.now()))
    elif(hive3_layer1_humid < Min_Humid_layer1):
        Humid_Anomaly.append("ALERT!!\nHive 3 Layer 1 humidity is at {0:.2f}%, which exceeds {1:.2f}% MINIMUM humidity set in the app.\nDate&Time: {2}".format(hive3_layer1_humid,Min_Humid_layer1,datetime.datetime.now()))
    #Hive 3 layer2 humid 
    if(hive3_layer2_humid > Max_Humid_layer2):
        Humid_Anomaly.append("ALERT!!\nHive 3 Layer 2 humidity is at {0:.2f}%, which exceeds {1:.2f}% MAXIMUM humidity set in the app.\nDate&Time: {2}".format(hive3_layer2_humid,Max_Humid_layer2,datetime.datetime.now()))
    elif(hive3_layer2_humid < Min_Humid_layer2):
        Humid_Anomaly.append("ALERT!!\nHive 3 Layer 2 humidity is at {0:.2f}%, which exceeds {1:.2f}% MINIMUM humidity set in the app.\nDate&Time: {2}".format(hive3_layer2_humid,Min_Humid_layer2,datetime.datetime.now()))
    
    

    if Temp_Anomaly:
        print("Anomalies:"+str(len(Temp_Anomaly)))
        for anomaly in range(len(Temp_Anomaly)):
            gsm.sendSMS(Temp_Anomaly[anomaly])
            client.publish(topic["alerts"],Temp_Anomaly[anomaly])
            
    if Humid_Anomaly:
        print("Anomalies:"+str(len(Humid_Anomaly)))
        for anomaly in range(len(Humid_Anomaly)):
            gsm.sendSMS(Humid_Anomaly[anomaly])
            client.publish(topic["alerts"],Humid_Anomaly[anomaly])
            
    
def Hive_weight_reporting():
    
   
    

    with open(directory["history"],'r') as f:
        history = json.load(f)
    hive1_weight = history['Reports'][-1]['Hive_1']['Weight']
    hive2_weight = history['Reports'][-1]['Hive_2']['Weight']
    hive3_weight = history['Reports'][-1]['Hive_3']['Weight']

    with open(directory["parameters"],'r') as f:
        params = json.load(f)
    Harvest_Weight = params['Parameters']['Harvest_Weight']
    """"Initial_Weight1": 4.01,
	"Initial_Weight2": 5.13,
	"Initial_Weight3": 5.81,"""
    
    with open(directory["initialWeights"],'r') as f:
        initiWeights = json.load(f)
    Initial_Weight1 = initiWeights['Initial_Weights']['Hive1']
    Initial_Weight2 = initiWeights['Initial_Weights']['Hive2']
    Initial_Weight3 = initiWeights['Initial_Weights']['Hive3']
    
    gain1 = hive1_weight-Initial_Weight1
    gain2 = hive2_weight-Initial_Weight2
    gain3 = hive3_weight-Initial_Weight3
    
    if( gain1 >= Harvest_Weight):
        report = "Hive 1 is ready for harvest. Weight gain is {0:0.2f}".format(gain1)
    if( gain2 >= Harvest_Weight):
        report = "Hive 2 is ready for harvest. Weight gain is {0:0.2f}".format(gain2)
    if( gain3 >= Harvest_Weight):
        report = "Hive 3 is ready for harvest. Weight gain is {0:0.2f}".format(gain3)
        
        
    report = "Bee Hive Weight Report: \n Hive 1 gain ={0:.2f}kg \n Hive 2 gain ={1:.2f}kg \n Hive 3 gain ={2:.2f}kg \n\n Date & Time:{3}".format(gain1,gain2,gain3,datetime.datetime.now())
    client.publish(topic["alerts"],report)
    
    gsm.sendSMS(report)

scheduler()

while True:
    
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        print("Main: Reporting Module: Program Interrupted!")
        sys.exit(0)


