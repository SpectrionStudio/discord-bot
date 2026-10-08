"""Module IA : parle au modèle local via Ollama."""

import ollama

MODELE = "gemma4:12b"
client_ollama = ollama.AsyncClient()


PROMPT_ASSISTANT = """Tu t'appelles Spectrion Studio Bot. Tu es l'assistant du serveur Discord de Spectrion Studio.
Tu tutoies tout le monde, sauf si on te demande explicitement de vouvoyer.
Tu peux utiliser des émojis quand la conversation s'y prête.
Tu réponds en français, en quelques phrases courtes (1 000 caractères maximum).
Si tu ne connais pas la réponse à une question, dis-le simplement plutôt que d'inventer."""


def charger_lore(chemin="lore.txt"):
    """Lit le fichier du roman. Renvoie un texte vide s'il n'existe pas."""
    try:
        with open(chemin, encoding="utf-8") as fichier:
            return fichier.read()
    except FileNotFoundError:
        return ""


LORE = charger_lore()

print(f"Lore chargé : {len(LORE)} caractères")

PROMPT_ROMAN = f"""Tu t'appelles Spectrion Studio Bot. Sur ce serveur, tu es le guide de l'univers du projet « The Release Of Riyo: Second Life ».
Tu tutoies tout le monde, sauf si on te demande explicitement de vouvoyer.
Tu peux utiliser des émojis quand la conversation s'y prête.
Tu réponds en français, en quelques phrases courtes (1 000 caractères maximum).

Pour répondre, tu t'appuies UNIQUEMENT sur les notes ci-dessous.
Tu peux résumer, reformuler et expliquer ces notes avec tes propres mots.
Si une information n'est pas dans les notes, dis clairement que tu ne la connais pas, sans rien inventer sur l'histoire, les personnages ou la suite.
Si on te demande la suite de l'histoire, la fin ou des secrets, réponds que ces informations ne sont pas révélées.

NOTES SUR L'UNIVERS :
{LORE}"""


async def demander(prompt_systeme, question):
    """Envoie une question au modèle et renvoie sa réponse (texte)."""
    reponse = await client_ollama.chat(
        model=MODELE,
         messages=[
            {"role": "system", "content": prompt_systeme},
            {"role": "user", "content": question},
        ],
        options={"num_predict": 400},
        think=False,
    )
   
    return reponse["message"]["content"]