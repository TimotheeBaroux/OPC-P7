# Implémentation d'un modèle de scoring
## Présentation
Ce projet a pour but .....


## Getting started
Sur le cloud
Attention : certains cookies sont nécessaires au bon fonctionnement de l'application et peuvent être bloqués par les antivirus.
En local lancer à la main le fichier de l'api via la commande `python APImaker.py` avant de lancer l'application avec la commande `streamlit run stats.py`

## Détails des fichiers
Fichier : `stats.py` : 
Fichier principal de l'application, à déployer via Streamlit : https://timotheebaroux-opc-p7-stats-4uplvx.streamlit.app/
Contient des statistiques descriptives sur l'ensemble des clients, et des comparaisons de quelques clients par rapport à l'ensemble.

Dossier : `pages` :
Dossier des fichiers secondaires de l'application, automatiquement pris en compte lors du déploiement de stats.py via Streamlit.

Fichier : `pages/app.py` :
Fichier secondaire de l'application, automatiquement pris en compte lors du déploiement de stats.py via Streamlit (ou en local)
Détermine si un client est éligible ou non à un prêt, et donne quelques explications supplémentaires sur l'égibilité.
Fonctionne sur un ensemble de clients pré-préparé.

Fichier : `APImaker.py` :
Fichier de l'Application Programming Interface, démarré par la ligne de code `subprocess.run([sys.executable, "APImaker.py"])` de app.py.
En local, 
Fait fonctionner le modèle sélectionné sur les données envoyées et renvoie soit une prédiction, soit les probabilités utilisées pour faire cette prédiction.

Fichier : `pipeline_final.pkl` :
Fichier du modèle entraîné utilisé par l'api.

Fichier : `X_ltrain.csv` :
Fichier de variables d'entraînement ayant servi à entrainer le modèle

Fichier : `y_ltrain.csv` :
Fichier de cibles d'entraînement ayant servi à entrainer le modèle

Fichier : `X_tract.csv` :
Fichier de données, sous-ensemble du jeu de données global, contenant les variables et les cibles.

Fichier : `requirements.txt` :
Fichier explicitant les extensions de python nécessaires au fonctionnement de l'application.