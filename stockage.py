"""Sauvegarde des avertissements (warns) dans un fichier JSON."""

import json
import os

# Le fichier est cherché à côté de stockage.py, où qu'on lance le bot
DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_WARNS = os.path.join(DOSSIER, "warns.json")


def charger_warns():
    """Lit warns.json et renvoie son contenu (un dictionnaire)."""
    if not os.path.exists(FICHIER_WARNS):
        return {}  # premier lancement : personne n'a encore été averti
    with open(FICHIER_WARNS, encoding="utf-8") as fichier:
        return json.load(fichier)


def sauvegarder_warns(warns):
    """Écrit le dictionnaire `warns` dans warns.json."""
    with open(FICHIER_WARNS, "w", encoding="utf-8") as fichier:
        json.dump(warns, fichier, ensure_ascii=False, indent=2)