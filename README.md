# Othello

Projet fait durant les Coding Week à CentraleSupelec.

## Principe du jeu

### Règles

L'othello est un jeu similaire au jeu de go : l'objectif est d'avoir le plus de territoires en capturant les pions de l'adversaire.
Les règles de l'Othello ont été récupéré sur le site www.eothello.com
Il est également possible de tester le jeu sur ce site

### Notre Othello

Ce repo contient plusieurs choses:
    - Un dossier gameOthello contenant le jeu. Il suffit de télécharger ce dossier pour profiter du jeu.
    - Un dossier server contenant le nécessaire pour créer un serveur de jeu pour le mode en ligne.
    - Un dossier tests contenant les fichiers python de test pour vérifier le bon fonctionnement du jeu.
    - Un dossier htmlcov contenant la couverture des tests proposés.

Notre jeu propose plusieurs possibilités:
    - Jouer contre une IA de difficulté variable
    - Jouer en local à 2, 3 ou 4 joueurs
    - Jouer en ligne.
    - Jouer à deux avec un mode Blitz: temps limité de jeu.

L'ensemble de ces modes de jeu sont disponibles dans le menu.

De plus, il est possible lors d'une partie locale de revenir en arrière.

### Tests unitaires
Chaque fichier de test est nommé selon quel fichier python est testé. L'ensemble des résultats se trouve dans htmlcov en ouvrant index.html . Seul le fichier `main.py` n'est pas testé car il sert simplement à vérifier les librairies installées et à lancer le jeu.

## Installation

### Prérequis

Avoir python 3.8 ou plus
Avoir la librairie pillow (`pip install pillow` ou `pip3 install pillow`)

### Jouer en local

Il suffit d'installer le dossier gameOthello et de lancer avec python `main.py`.

### Jouer en ligne

Il suffit de cliquer sur le bouton join game pour créer/rejoindre une partie. Le nom de la partie est par défaut aléatoire mais peut être choisi. Il faut mettre le code d'une partie existante non commencée pour la rejoindre.

Par défaut, le jeu se connecte à localhost, il faut donc lancer `server.py` sur la même machine. Cependant, il est possible de changer l'ip du server dans `network.py` pour le connecter à un autre que vous pouvez héberger.

### Héberger son serveur

Il faut télécharger le dossier server et lancer `server.py` sur votre serveur. Par défaut, le client se connecte sur le port 5555, donc si vous souhaitez en mettre un autre, il faudra changer ce port dans `network.py` sur le jeu client dans `network.py`.
De plus, il faut changer l'ip par défaut dans la class Network pour qu'il se connecte au serveur.

Pour jouer depuis un réseau externe, il faut ouvrir le port 5555 sur sa box pour le rediriger vers la machine.


## Images du jeu

### Menu

![image](https://github.com/Aul16/Othello/assets/39156836/c1aa1064-80ac-4def-8844-264e07aaa27a)

### Partie à 2

![image](https://github.com/Aul16/Othello/assets/39156836/683ebd3f-feaa-4d71-9340-2ec7f2dfc16f)

### Partie à 3

![image](https://github.com/Aul16/Othello/assets/39156836/d847c1b7-7a09-4c6f-897f-b3f0c4530ccb)

