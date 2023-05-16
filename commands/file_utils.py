import json
from structures.module1 import CommandHistory


# fichier json
user_histories_file = "user_histories.json"

#fonction qui Charge les données d'un fichier JSON et renvoie un dictionnaire.
def load_data_from_json(file_name):
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# fonction qui Sauvegarde les données dans un fichier JSON.
def save_data_to_json(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f)

