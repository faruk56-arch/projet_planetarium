from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json
from uuid import uuid4


app = Flask(__name__)

# Configuration du producteur Kafka avec confluent_kafka
producer_config = {
    'bootstrap.servers': 'kafka:9092'  # Adresse de votre serveur Kafka
}
producer = Producer(producer_config)

# Liste pour stocker les decouvertes de planetes
planets_discoveries = []

@app.route('/discover_planet', methods=['POST'])
def discover_planet():
    data = request.json
    required_fields = ["Name","Num_Moons","Minerals","Gravity","Sunlight_Hours","Temperature","Rotation_Time","Colonisable", "Water_Presence"
]
    
    # Validation des donnees
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    # Ajout d'un ID unique à la decouverte
    data["ID"] = str(uuid4())
    planets_discoveries.append(data)
    
    # Fonction de callback pour les erreurs de production
    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    # Envoi des donnees à Kafka
    producer.produce('topic_1', key=data["ID"], value=json.dumps(data).encode('utf-8'), callback=delivery_report)
    producer.flush()  # Attendre que tous les messages soient envoyes

    return jsonify({"message": "Planet discovery added successfully!", "discovery": data}), 201

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5550)