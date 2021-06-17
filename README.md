# mwe-extraction
Implémentation de systèmes de reconnaissance d'unités polylexicales pour l'étiquetage morphosyntaxique. Nous utilsons deux modèles principaux : une simple **regression logistique multonomiale**, et un modèle **crf**. Une amélioration que nous proposons est d'intégrer, sous forme de caractéristiques, des paramètres estimés en amont sur un lexique d'unités polylexicales extraites du corpus **_lefff_** (https://www.labri.fr/perso/clement/lefff/)

## Comment lancer le programme

D'abord, se placer dans le dossier racine du projet, ensuite lancer cette commande :

```console
user@name:~$ python3 mwe_extraction --corpus --split_infos
```

où --corpus est le corpus et split_infos le fichier qui contient les infos en découpage test, train, dev. Dans le cas du crf amélioré, il faut ajouter le paramètre -w les paramètres estimés en amont (vparametres) servant d'amélioration

Par exemple si on veut test le crf amélioré :

```console
user@name:~/mwe-extraction$ python3 src/crf-ameliore/mwe_extraction.py --corpus data/sequoia.surf.parseme_.frsemcor --split_infos data/sequoia_split_info --w src/crf-ameliore/vparametres.json 
```

## Ce qui est recquis
* scikit-learn (https://scikit-learn.org/stable/)
* sklearn-crfsuite (https://sklearn-crfsuite.readthedocs.io/en/latest/)
