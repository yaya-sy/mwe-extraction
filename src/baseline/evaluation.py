""" Ce module implémente un ensemble de statistiques pour évaluer les prédictions
de nos classificateurs structurés """

import numpy as np
class Evaluation :
  """Cette classe implémente une classe qui permet de produire des \
  statistiques concernant la capacité du système à reconnaître les \
  unités polylexicales.

  Paramaters
  ----------
  - clf: sklearn_crfsuite.estimator.CRF
    le modèle CRF avec ses paramètres estimés.
  - y_golds_test: list
    les classes golds du corpus de test.
  - feats_test: list
    les caractéristiques extraites dans le corpus test.
  - X_test : np.array
    matrice de données pour le test
  - feats_train: list
    les caractéristiques extraites dans le corpus test.
  - X_train : np.array :
    matrice d'entraînement
  - y_golds_train: list
    les classes golds du corpus de train

  Methods
  -------
  - test_predict :
    return les prédictions du classifieur sur le cotpus de test
  - b_i_precision :
    la précision du modèle sur les unités polylexicales.
  - b_i_rappel :
    le rappel du modèle sur les unités polylexicales
  - oov :
    retourne le pourcentage de mots inconnus du corpus de train \
    dans le corpus de test
  - precision_oov :
    retourne la précision du modèle sur les mots inconnus
  """
  def __init__(self,
               clf,
               y_golds_test: list,
               feats_test: list,
               X_test : np.array,
               feats_train: list,
               X_train,
               y_golds_train: list) -> None :
    self.clf = clf
    self.feats_test = feats_test
    self.X_test = X_test
    self.y_preds_test = self.clf.predict(self.X_test)
    self.y_golds_test = y_golds_test
    self.mcs_test = self.__map(self.feats_test, self.y_golds_test)
    self.tcs_test = [y for y in self.__enumerate_tags(self.y_golds_test) if len(y) > 1]

    self.feats_train = feats_train
    self.X_train = X_train
    self.y_preds_train = self.clf.predict(self.X_train)
    self.y_golds_train = y_golds_train
    self.mcs_train = self.__map(self.feats_train, self.y_golds_train)
    self.tcs_train = [y for y in self.__enumerate_tags(self.y_golds_train) if len(y) > 1]

  def __regroupe_mots_composes(self, tags: list) :
    """
    Fonction qui regrouppe les mots composés en liste.
    Pour une entrée comme [B_DET, B_NOUN, I_DET, I_NOUN, B_VERB], va renvoyer [[B_DET], [B_NOUN, I_DET, I_NOUN], [B_VERB]]
    """
    l = len(tags)
    liste = []
    i = 0
    while i <= l - 1 :
      inside = [tags[i]]
      j = i + 1
      find = True
      while find :
        if j < l and "I_" in tags[j] :
          inside.append(tags[j])
        else :
          find = False
        j += 1
      i = j - 1
      liste.append(inside)
    return liste


  def __enumerate_tags(self, tags) :
    """
    Fonction qui prend entrée une liste de tags, où le i^eme tag
    est le tag du i^eme mot, et retourne une liste où ces tags sont
    énumérés et les mots composés regroupé

    Parameters
    ----------
    - tags : list
      liste des tags

    Returns
    -------
    - list :
      la liste de tags énumérés et regroupée en mots composés.
    """
    return self.__regroupe_mots_composes([t + "_" + str(i) for i, t in enumerate(tags)])


  def b_i_precision(self: object) -> float :
    """
    Fonction qui calcule la précision du classifieur sur le corpus de test.

    Returns
    -------
    - float : taux de bonnes classifications
    """

    preds = [y for y in self.__enumerate_tags(self.y_preds_test) if len(y) > 1]
    golds = [y for y in self.__enumerate_tags(self.y_golds_test) if len(y) > 1]

    bons, tot = zip(*((int(pred in golds), 1) for pred in preds))
    return sum(bons) / sum(tot)

  def b_i_rappel(self: object) -> float :
    """
    Fonction qui calcule le rappel du classifieur sur le corpus de test.

    Returns
    -------
    - float : rappel
    """
    preds = [y for y in self.__enumerate_tags(self.y_preds_test) if len(y) > 1]
    golds = [y for y in self.__enumerate_tags(self.y_golds_test) if len(y) > 1]

    return sum(1 if pred in golds else 0 for pred in preds) / len(golds)

  def __map(self: object, feats, tags) -> tuple :
    mots = []
    for mot in feats :
      for ft in mot :
        if ft.startswith("mot") :
          mots.append(ft.split("=")[-1])
    print(len(mots))
    mots_composes = []

    for tag_compose in [y for y in self.__enumerate_tags(tags) if len(y) > 1] :
      mot_compose = []
      for tag in tag_compose :
        mot_compose.append(mots[int(tag.split('_')[-1])])
      mots_composes.append(("_".join(mot_compose), tag_compose))
    return mots_composes

  def oov(self: object) -> float :
    """
    calcule le pourcentage de mots inconnus.

    Returns
    -------
    - float : le pourcentage de mots inconnus dans le  \
      le corpus test.
    """
    mcs_test = [mc for (mc, tc) in self.mcs_test]
    mcs_train = [mc for (mc, tc) in self.mcs_train]
    pst, tot = zip(*((int(mct in mcs_train), 1) for mct in mcs_test))

    return sum(pst) / sum(tot)

  def precision_oov(self: object) -> float :
    """
    calcule la précision du système sur les mots non vus \
    en apprentissage

    Returns
    -------
    - float : la précision sur les mots non vus en apprentissage
    """
    mcs_ts, golds = zip(*self.mcs_test)
    mcs_tr = [mc for (mc, tc) in self.mcs_train]
    mcs, golds = zip(*((mc, ct) for (mc, ct) in self.mcs_test if mc not in mcs_tr))

    preds = [pred for pred in self.__enumerate_tags(self.y_preds_test) if len(pred) > 1]

    bons, tot = zip(*((int(pred in golds), 1) for pred in preds))

    return sum(bons) / sum(tot)

  def fscore(self: object) -> float:
    """
    Fonction qui calcule le fscore du classifieur sur le corpus de test.

    Returns
    -------
    - float : fscore
    """
    p = self.b_i_precision()
    r = self.b_i_rappel()

    return 2 * ((p * r) / (p + r))
