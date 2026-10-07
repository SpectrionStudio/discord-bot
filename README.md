# Spectrion Studio

Le bot sert pour différentes fonctionnalités que ce soit en communautaire ou bien sur la modération.
Il va permettre de pouvoir se reposer sur lui et non sur des bots d'une provenance inconnue ou bien sur les bots utilisés par la grande majorité des owners discord.

Le projet vise à terme à proposer des outils de modération, dont une protection contre les raids.

## Prérequis

- Python 3.10 ou plus récent
- Une application Discord créée sur le [portail développeurs](https://discord.com/developers/applications), avec son bot et son token
- Le Server Members Intent activé (menu Bot → Privileged Gateway Intents), nécessaire pour le message de bienvenue

## Installation

1. Cloner le dépôt :
```bash
   git clone https://github.com/SpectrionStudio/discord-bot.git
   cd discord-bot
```
2. Installer les dépendances :
```bash
   pip install -r requirements.txt
```
3. Copier `.env.example` en `.env` et le remplir avec votre token et l'identifiant de votre serveur.
4. Lancer le bot :
```bash
   python bot.py
```

## Permissions du bot

Pour fonctionner, le bot a besoin des permissions suivantes sur le serveur pour le moment :

- Envoyer des messages et intégrer des liens
- Joindre des fichiers (image de bienvenue)
- Gérer les messages et lire l'historique (commande `/clear`)

Il doit être invité avec les scopes `bot` et `applications.commands`.

## Configuration du serveur

Le message de bienvenue est envoyé dans le **salon des messages système** du serveur (Paramètres du serveur → Général). Sans salon défini, le bot n'envoie rien.

 

## Fonctionnalités

Pour le moment j'ai pu travailler quelques commandes dont : 

- /ping
Ping le bot pour lui parler

- /serveurinfo
Informations sur le serveur

- /userinfo
Information sur l'utilisateur recherché

- /help
Toutes les commandes que je peux exécuter !

- /linktree
Obtenez tous nos réseaux grâce à cette commande !

- /clear
Permet de supprimer un nombre déterminé de messages

Mais aussi des messages de bienvenue pour les nouveaux membres.

## Aperçu

<img width="479" height="212" alt="serveurinfo" src="https://github.com/user-attachments/assets/3f312459-0311-4209-bb1a-d97a05b4065c" />

<img width="623" height="236" alt="userinfo" src="https://github.com/user-attachments/assets/77526da8-4ae7-40cd-b1f8-c601ba33840b" />

<img width="460" height="400" alt="help" src="https://github.com/user-attachments/assets/1de8f89d-ae7f-4f70-b9ed-055cc6394609" />

<img width="467" height="374" alt="linktree" src="https://github.com/user-attachments/assets/da8c1721-1b8e-460a-874e-5a0bb0431376" />

## Technologies

Utilisation principalement de Python ainsi que de discord.py pour le codage de ce bot discord pour le moment.

## Ce que j'ai appris

J'ai pu apprendre différentes choses sur ce codage. Notamment la construction des embed dont je ne connaissais pas du tout le principe. Mais aussi la création de commande que ce soit par évent ou par appel de commande.
Beaucoup de notions que je ne connaissais pas du tout car je n'avais jamais tenté de coder mon propre bot discord dans le passé. Donc beaucoup de choses nouvelles.
Mais aussi des termes que j'ai pu retravailler comme les f string qui ne m'avaient pas manqué.


  > L'illustration de bienvenue n'est pas incluse dans le dépôt : ajoutez votre propre image dans `images/bienvenue.png`.