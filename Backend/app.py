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

# Liste pour stocker les découvertes de planètes
planets_discoveries = []

@app.route('/discover_planet', methods=['POST'])
def discover_planet():
    data = request.json
    required_fields = ["Nom", "Découvreur", "Date de Découverte", "Masse", "Rayon", "Distance", "Type", "Statut", 
                    "Atmosphère", "Température Moyenne", "Période Orbitale", "Nombre de Satellites", "Présence d’Eau"]
    
    # Validation des données
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    # Ajout d'un ID unique à la découverte
    data["ID"] = str(uuid4())
    planets_discoveries.append(data)
    
    # Fonction de callback pour les erreurs de production
    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    # Envoi des données à Kafka
    producer.produce('topic_1', key=data["ID"], value=json.dumps(data).encode('utf-8'), callback=delivery_report)
    producer.flush()  # Attendre que tous les messages soient envoyés

    return jsonify({"message": "Planet discovery added successfully!", "discovery": data}), 201

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5550)