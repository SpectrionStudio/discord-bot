import ollama

PROMPT_SYSTEME = """Tu t'appelles Spectrion Studio Bot. Tu es l'assistant du serveur Discord de Spectrion Studio.
Tu tutoies tout le monde, sauf si on te demande explicitement de vouvoyer.
Tu peux utiliser des émojis quand la conversation s'y prête.
Tu réponds en français, en quelques phrases courtes (1 000 caractères maximum).
Si tu ne connais pas la réponse à une question, dis-le simplement plutôt que d'inventer."""

historique = [
    {"role": "system", "content": PROMPT_SYSTEME},
]
print(historique[0])
while True:

    question = input("Vous : ")
    if question == "quit":
        break

    historique.append({"role": "user", "content": question})
    reponse = ollama.chat(model="gemma4:12b", messages=historique)
    texte = reponse["message"]["content"]

    historique.append({"role": "assistant", "content": texte})
    print("IA :", texte)