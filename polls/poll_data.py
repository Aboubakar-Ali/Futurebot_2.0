import json

# Fonction qui Charge les données d'un fichier JSON et renvoie un dictionnaire.
def load_data_from_json(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Fonction qui Sauvegarde les données dans un fichier JSON.
def save_data_to_json(file_name, data):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


polls_data = load_data_from_json("polls.json")
poll_names_data = load_data_from_json("poll_names.json")

# Charge le fichier JSON des sondages
polls = {int(msg_id): (int(author_id), max_votes, {int(user_id): votes for user_id, votes in user_votes.items()})
         for msg_id, (author_id, max_votes, user_votes) in polls_data.items()}

# stocker les noms des sondages et leurs identifiants de message 
poll_names = {name: int(msg_id) for name, msg_id in poll_names_data.items()}
