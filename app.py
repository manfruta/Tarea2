from flask import Flask, request, jsonify
from kafka import KafkaConsumer, KafkaProducer
import json
from kafka import TopicPartition



app = Flask(__name__)

@app.route('/orden', methods = ['POST'])
def nuevaOrden():
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'), bootstrap_servers=['localhost:9092'])
    producer.send('ordenes', request.json)
    #producer.flush()
    print("Produciendo: ",request.json)
    return "EL productor funciona"


contador = 0
@app.route('/diario')
def resumenDiario():
    global contador 
    consumer = KafkaConsumer('ordenes',bootstrap_servers=['localhost:9092'],value_deserializer=lambda m: json.loads(m.decode('ascii')),
    auto_offset_reset='earliest', enable_auto_commit=False)
    partitions = [TopicPartition('ordenes',p) for p in consumer.partitions_for_topic('ordenes')]
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
            if(len(data)==0):
                data['vendedor'].append({'nombre vendedor': msg.value['nombre vendedor'],'correo vendedor': msg.value['correo vendedor'],'sopaipas totales': msg.value['cantidad de sopaipas']})
                data['cocineros'].append({'nombre cocinero': msg.value['nombre cocinero'],'correo cocinero': msg.value['correo cocinero'],'sopaipas totales': msg.value['cantidad de sopaipas']})       
            else:
                count = 0
                print(len(data['vendedor']))
                for i in data['vendedor']: 
                    if(msg.value['nombre vendedor'] == i.value['nombre vendedor']):
                        i.value['sopaipas totales'] = msg.value['cantidad de sopaipas'] + i.value['sopaipas totales']
                        break
                    else:
                        if(count == len(data['vendedor'])):
                            data['vendedor'].append({'nombre vendedor': msg.value['nombre vendedor'],'correo vendedor': msg.value['correo vendedor'],'sopaipas totales': msg.value['cantidad de sopaipas']})
                            break
                
                count = 0
                for i in data['cocineros']: 
                    if(msg.value['nombre vendedor'] == i.value['nombre vendedor']):
                        i.value['sopaipas totales'] = msg.value['cantidad de sopaipas'] + i.value['sopaipas totales']
                        break
                    else:
                        if(count == len(data['cocineros'])):
                            data['cocineros'].append({'nombre cocinero': msg.value['nombre cocinero'],'correo cocinero': msg.value['correo cocinero'],'sopaipas totales': msg.value['cantidad de sopaipas']})
                            break
    
    return "EL consumidor funciona"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


