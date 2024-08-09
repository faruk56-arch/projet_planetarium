- TP Planetarium 
    
      Partie 1 : Backend Flask
    
    1.  Création du Backend Flask  :
        - Créez une application Flask capable de recevoir des informations de découvertes de planètes via des requêtes HTTP POST.
        - Chaque découverte de planète devra inclure les informations définies dans le modèle de données.
    2. Validation des Données  :
        - Implémentez une validation pour vérifier que toutes les informations requises sont présentes et correctes.
    3.  Envoi vers Kafka  :
        - Configurez l’application Flask pour envoyer les données reçues vers un pipeline Kafka.
    
       Exemple  de modèle de découverte de planète :
    
    -  ID  : Identifiant unique de la découverte
    -  Nom  : Nom de la planète
    -  Découvreur  : Nom du scientifique ou équipe ayant découvert la planète
    -  Date de Découverte  : Date de la découverte
    -  Masse  : Masse de la planète (en multiples de la masse terrestre)
    -  Rayon  : Rayon de la planète (en multiples du rayon terrestre)
    -  Distance  : Distance de la planète par rapport à la Terre (en années-lumière)
    -  Type  : Type de la planète (ex. géante gazeuse, terrestre, naine)
    -  Statut  : Statut de la planète (confirmée, non confirmée, potentielle)
    -  Atmosphère  : Composition atmosphérique de la planète (ex. azote, oxygène)
    -  Température Moyenne  : Température moyenne à la surface de la planète (en Celsius)
    -  Période Orbitale  : Durée de l'orbite autour de son étoile (en jours terrestres)
    -  Nombre de Satellites  : Nombre de satellites naturels connus
    -  Présence d’Eau  : Indication de la présence d’eau sous forme liquide (oui/non)
    
      Partie 2 : Pipeline Kafka
    
    1.  Mise en Place de Kafka  :
        - Installez et configurez Kafka.
        - Créez un topic Kafka pour les découvertes de planètes.
    2.  Production de Messages  :
        - Configurez le backend Flask pour produire des messages dans le topic Kafka lorsqu’une nouvelle découverte de planète est reçue.
    
      Partie 3 : Traitement avec Apache Spark
    
    1.  Configuration de Spark  :
        - Installez et configurez Apache Spark.
        - Configurez Spark pour consommer les messages du topic Kafka.
    2.  Traitement des Données  :
        - Développez un script Spark pour analyser les données des découvertes de planètes.
        - Calculez des statistiques agrégées comme la moyenne de la masse des planètes, la distribution des types de planètes, etc.
    3.  Traitements Avancés et Analyses  :
        - Analyse des relations entre les différentes caractéristiques des planètes pour identifier des tendances ou des anomalies.
        - Calcul des corrélations entre la présence d’eau et d’autres caractéristiques comme la distance par rapport à la Terre et la température moyenne.
        - Identification des clusters de planètes similaires à l'aide d'algorithmes de clustering.
        - Prédiction de la possibilité d’habitabilité des planètes en utilisant des algorithmes de machine learning.
    4.  Intégration d'un Modèle d'IA  :
        - Implémentez un modèle d'IA pour effectuer des prédictions basées sur les données des découvertes de planètes.
        - Par exemple, prédire la probabilité qu’une planète soit habitable basée sur ses caractéristiques.
    5.  Envoi des Résultats vers HDFS  :
        - Configurez Spark pour stocker les résultats des analyses et des prédictions dans HDFS.
    6.  Stockage Structuré dans Hive  :
        - Configurez Spark pour également stocker les données transformées dans Hive pour une gestion structurée et des requêtes SQL.
    
      Partie 4 : Stockage dans HDFS et Hive
    
    1.  Configuration de HDFS  :
        - Installez et configurez Hadoop pour utiliser HDFS.
    2.  Stockage des Résultats  :
        - Assurez-vous que les résultats des analyses et des prédictions sont correctement stockés dans HDFS.
    3.  Configuration de Hive  :
        - Installez et configurez Hive.
        - Créez une base de données et des tables Hive pour stocker les données structurées des découvertes de planètes.
    4.  Stockage dans Hive  :
        - Configurez Spark pour sauvegarder les données dans les tables Hive après le traitement.