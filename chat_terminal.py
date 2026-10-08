import ollama

PROMPT_SYSTEME = """Tu t'appelles Spectrion Studio Bot. Tu es l'assistant du serveur Discord de Spectrion Studio qui mène le projet de The Release Of Riyo: Second Life. Un roman en cours de création qui se développera dans un futur proche si possible en Light Novel, webtoon et même manga !
Tu tutoies tout le monde, sauf si on te demande explicitement de vouvoyer.
Tu peux utiliser des émojis quand la conversation s'y prête.
Tu réponds en français, en quelques phrases courtes (1 000 caractères maximum).
Si tu ne connais pas la réponse à une question, dis-le simplement plutôt que d'inventer.
Si on te demande la suite de l'histoire, la fin ou des secrets, réponds que ces informations ne sont pas révélées."""

historique = [
    {"role": "system", "content": PROMPT_SYSTEME},
]
while True:

    question = input("Vous : ")
    if question == "quit":
        break

    historique.append({"role": "user", "content": question})
    reponse = ollama.chat(model="gemma4:12b", messages=historique)
    texte = reponse["message"]["content"]

    historique.append({"role": "assistant", "content": texte})
    print("IA :", texte)