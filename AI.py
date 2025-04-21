import openai
from openai import OpenAI

client = OpenAI(api_key="MA_CLE_SECRETE_API")
def repondre(tache):
    messages=[
        {"role": "system", "content": (
            "Tu es un assistant personnel expert en productivité, psychologie, gestion du temps et optimisation des tâches. "
            "Pour chaque tâche fournie par l'utilisateur, tu dois :\n"
            "- Analyser la tâche pour en comprendre les objectifs et les contraintes.\n"
            "- Proposer une méthode ou un plan d'action clair pour l'accomplir efficacement.\n"
            "- Suggérer des outils ou techniques pertinents si nécessaire.\n"
            "- Motiver l'utilisateur avec une phrase encourageante.\n"
            "Ta réponse doit être concise (3 à 5 phrases), structurée et adaptée au contexte de la tâche."
            "Qui plus est considère que le message que tu vas écrire sera montré soit sur un terminal de réponse python de Pycharm 2025, soit sur une interface graphique assez basique de TKinter."
        )},
        {"role": "user", "content": f"Tâche : {tache}"}
    ]
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=messages,
    temperature=0.65,
    max_tokens=250,
    store=True,
    )
    return completion.choices[0].message.content

