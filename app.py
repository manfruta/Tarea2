from flask import Flask, request, jsonify
from kafka import KafkaConsumer, KafkaProducer
import json
from kafka import TopicPartition
import smtplib

app = Flask(__name__)

@app.route('/nuevaorden', methods = ['POST'])
def nuevaOrden():
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'), bootstrap_servers=['localhost:9092'])
    producer.send('order', request.json)
    #producer.flush()
    #print("Produciendo: ",request.json)
    return "EL productor funciona"

contador = 0
@app.route('/resumenDiario')
def resumenDiario():
    global contador 
    consumer = KafkaConsumer('order',bootstrap_servers=['localhost:9092'],value_deserializer=lambda m: json.loads(m.decode('ascii')),
    auto_offset_reset='earliest', enable_auto_commit=False)
    partitions = [TopicPartition('order',p) for p in consumer.partitions_for_topic('order')]
    last_offset_per_partition = consumer.end_offsets(partitions)
    numero = list(last_offset_per_partition.values())[0] 

    vector = []

    if contador == 0:
        for message in consumer:
            vector.append(message)
            contador+=1
            if contador==numero:
                break
    else:
        if numero>contador:
            for message in consumer:
                if message.offset+1==contador+1:
                    vector.append(message)
                    contador+=1
                    if contador==numero:
                        break
    
    data = {}
    data['vendedor'] = []
    data['cocineros'] = []
    if (len(vector)!=0):
        for msg in vector:
            ordenes = 0
            if(len(data['vendedor'])!=0 and len(data['cocineros'])!=0):
                count = 0
                for i in data['vendedor']: 
                    if(msg.value['nombre vendedor'] == i['nombre vendedor']):
                        i['sopaipas totales'] = msg.value['cantidad de sopaipas'] + i['sopaipas totales']
                        i['ordenes'] = i['ordenes'] + 1
                        break
                    else:
                        if(count == len(data['vendedor'])-1):
                            ordenes = 1
                            data['vendedor'].append({'nombre vendedor': msg.value['nombre vendedor'],'correo vendedor': msg.value['correo vendedor'],'sopaipas totales': msg.value['cantidad de sopaipas'], 'ordenes':ordenes})
                            break   

                count = 0
                for i in data['cocineros']:  
                    if(msg.value['nombre cocinero'] == i['nombre cocinero']):
                        i['sopaipas totales'] = msg.value['cantidad de sopaipas'] + i['sopaipas totales']
                        i['ordenes'] = i['ordenes'] + 1
                        break
                    else:
                        if(count == len(data['cocineros'])-1):
                            ordenes = 1
                            data['cocineros'].append({'nombre cocinero': msg.value['nombre cocinero'],'correo cocinero': msg.value['correo cocinero'],'sopaipas totales': msg.value['cantidad de sopaipas'], 'ordenes':ordenes})
                            break        
            else:    
                ordenes = 1
                data['vendedor'].append({'nombre vendedor': msg.value['nombre vendedor'],'correo vendedor': msg.value['correo vendedor'],'sopaipas totales': msg.value['cantidad de sopaipas'],'ordenes':ordenes})
                data['cocineros'].append({'nombre cocinero': msg.value['nombre cocinero'],'correo cocinero': msg.value['correo cocinero'],'sopaipas totales': msg.value['cantidad de sopaipas'],'ordenes':ordenes})

    data2 = {}
    data2['personas'] = []            

    for i in data['vendedor']:
        data2['personas'].append({'nombre': i['nombre vendedor'],'correo':i['correo vendedor'],'sopaipas totales':i['sopaipas totales'],'tipo':'vendedor','ordenes':i['ordenes']})

    for i in data['cocineros']:
        data2['personas'].append({'nombre': i['nombre cocinero'],'correo':i['correo cocinero'],'sopaipas totales':i['sopaipas totales'],'tipo':'cocinero','ordenes':i['ordenes']})

    producer2 = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'), bootstrap_servers=['localhost:9092'])
    for i in data2['personas']:
        producer2.send('dailysummary', i)
    
    return "EL consumidor funciona"


contador2= 0
@app.route('/MandarEmail')
def MandarEmail():
    global contador2 
    consumer = KafkaConsumer('dailysummary',bootstrap_servers=['localhost:9092'],value_deserializer=lambda m: json.loads(m.decode('ascii')),
    auto_offset_reset='earliest', enable_auto_commit=False)
    partitions = [TopicPartition('dailysummary',p) for p in consumer.partitions_for_topic('dailysummary')]
    last_offset_per_partition = consumer.end_offsets(partitions)
    numero = list(last_offset_per_partition.values())[0] 

    vector = []

    if contador2 == 0:
        for message in consumer:
            vector.append(message)
            contador2+=1
            if contador2==numero:
                break
    else:
        if numero>contador2:
            for message in consumer:
                if message.offset+1==contador2+1:
                    vector.append(message)
                    contador2+=1
                    if contador2==numero:
                        break
    
    servidor = smtplib.SMTP('smtp.gmail.com',587)
    servidor.starttls()
    servidor.login('yeyoldof@gmail.com',"yeyoldo123")
    correo = ""
    nombre = ""
    total = ""
    enviar = ""
    tipo = ""
    accion = ""
    ordenes = ""
    for i in vector:
        nombre = i.value['nombre']
        total = str(i.value['sopaipas totales'])
        correo = i.value['correo']
        tipo = i.value['tipo']
        ordenes = str(i.value['ordenes'])

        if(tipo=='vendedor'):
            accion = " hoy como vendedor vendiste "
        else:
            accion = " hoy como cocinero cocinaste "

        enviar = "Hola "+nombre+accion+total+" en "+ordenes+" ordenes"
        print(enviar)

        servidor.sendmail("yeyoldof@gmail.com",correo,enviar)
    servidor.quit()

    return "Mensaje enviado rey"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


