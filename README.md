# mwe-extraction
Implémentation de systèmes de reconnassance d'unités polylexicales pour l'étiquetage morphosyntaxique. Nous utilsons deux modèles principaux : une simple **regression logistique multonomiale**, et un modèle **crf**. Une amélioration que nous proposons est d'intégrer, sous forme de caractéristiques, des paramètres estimés en amont sur un lexique d'unités polylexicales extraites du corpus **_lefff_** (https://www.labri.fr/perso/clement/lefff/)

## lancer le programme

D'abord, se placer dans le dossier du modèle que l'on veut tester, ensuite lancer cette commande :

```console
user@name:~$ mwe_extraction --corpus
```
