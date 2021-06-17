"""Ce module extrait les caractéristiques lexicales et syntaxiques de chaque mot."""
from itertools import chain
import json

class Features(object) :
  """Cette classe permet d'extraire les caractéristiques lexicales
  et syntaxiques des mots.

  Parameters
  ----------
  - data : ReadCorpus
    instance de la classe ReadCorpus qui permet de retourner des tuples
    de (phrase, tags)
  - span_w : int
    la taille des affixes à cosidérer pour les caractéristiques morphologiques
    des mots.
  - span_s : int
    la taille de la fenêtre de contexte à considérer pour les mots précédents
    et suivants du mot courant.
  - w :
    paramètres estimés en amont

  Methodes
  --------
  - features :
    renvoie les caractéristiques d'un mot à une position dans une phrase
  - get_features :
    renvoie l'ensemble des caractéristiques extraites du corpus
  """

  def __init__(self : object,
               train: list,
               test: list,
               dev: list,
               span_w: int,
               span_s: int,
               w : dict) -> object:
    self.train = train
    self.test = test
    self.dev = dev
    self.span_w = span_w
    self.span_s = span_s
    self.beg, self.end = list(zip(*((f"@BEG{i}@", f"@END{i}@")  for i in range(span_s))))
    self.beg, self.end = list(self.beg), list(self.end)
    self.w = w

  def features(self: object,
               phrase: list,
               span_w: int,
               span_s: int,
               tags: list,
               position: int) -> tuple :
    """
    Fonction qui extrait les features en créant un dictionnaire.
    Pour chaque mot on regarde :
        - pref1 = son préfixe de longueur 1
        - pref2 = son préfixe de longueur 2
        - pref3 = son su
        - etc
        - suff1 = son suffixe de longueur 1
        - suff2 = son suffixe de longueur 2
        - suff3 = son suffixe de longueur 3
        - etc.
    on regarde aussi les span_s mots précedents et les span_s suivants :
        - w_1 = le mot suivant le mot courant
        - w_-1 = le mot précédent le mot courant

    Parametres
    ----------
    - phrase : list
      la phrase courante dans le corpus
    - span_w : int
      la taille des affixes à cosidérer pour les caractéristiques morphologiques
      des mots.
    - span_s : int
      la taille de la fenêtre de contexte à considérer pour les mots précédents
      et suivants du mot courant.
    - tags : list
      la liste de tags correspondants aux tags des mots de la phrase courante
    - position : int
      position dans la phrase courante.

    Returns
    -------
    - tuple :
      les caractéristuques du mot à la position courante et son tag
    """
    span_s += 1
    l = len(phrase)
    p = self.beg + phrase + self.end
    t = self.beg + tags + self.end
    features = {}
    if p[position] not in self.beg + self.end : #and mot in mc and mot not in mots :
        for spann in chain.from_iterable([(-i, i) for i in range(1, span_s)]) :
            features.update({"w_" + str(spann) + " = " + p[position + spann] : 1})
            if spann < 0 : features.update({"t_" + str(spann) + " = " + t[position + spann] : 1})

        for span in chain.from_iterable([(-i, i) for i in range(1, span_w + 1)]):
            if span < 0 :
                if len(p[position]) >= abs(span) :
                    features.update({"pref" + str(abs(span)) + "=" + p[position][:-span] : 1})
                else :
                    features.update({"pref" + str(abs(span)) + "=" + "HayDara" : 1})
            else :
                if len(p[position]) >= abs(span) :
                    features.update({"suff" + str(span) + "=" + p[position][-span:] : 1})
                else :
                    features.update({"suff" + str(abs(span))  + "=HayDara" : 1})

        features.update({"maj" + "=" + str(p[position][0].isupper()) : 1})
        features.update({"mot" + "=" + p[position] : 1})
        features.update({"Maj" + "=" + str(p[position].isupper()) : 1})
        pr = ""
        sv = ""
        for k,v in features.items() :
          if k.startswith("w_-1") :
            pr = k
          if k.startswith("w_1") :
            sv = k
        m_pr = pr.split("= ")[-1]
        m_sv = sv.split("= ")[-1]
        # be = score(dico_features([m_pr, p[position], m_sv]))[0]
        ins = score(dico_features([m_pr, p[position], m_sv]), self.w)[0]
        non = score(dico_features([m_pr, p[position], m_sv]), self.w)[1]

        features.update({"ins" : int(ins > 0.7)})
        features.update({"non" : int(non > 0.7)})
        features.update({"compose" : int(ins > non)})

        # features.update({"biais" : 1})
    if bool(features) :
        return features, t[position]

  def __get_features(self: object, corpus: list) -> tuple :
    # retourne les caractéristiques des mots de chaque phrase
    phrase_fts = []
    phrase_golds = []
    for phrase, labels in corpus :
        fts = []
        golds = []
        if len(phrase) <= 1: continue
        for i in range(len(phrase)) :
          f = self.features(list(phrase), self.span_w, self.span_s, list(labels), i)
          if f != None :
            f,g = f
            fts.append(f)
            golds.append(g)
        phrase_fts.append(fts)
        phrase_golds.append(golds)
    return phrase_fts, phrase_golds

  def get_features(self: object) -> tuple:
    """
    Fonction qui renvoie les caractéristiques des corpus de train, test et dev

    Returns
    -------
    - tuple :
      Les caractéristiques sous forme de liste de listes pour les trois corpus.
      Chaque liste représente les caractéristiques des mots d'une phrase
    """
    return self.__get_features(self.train), self.__get_features(self.test), self.__get_features(self.dev)

def dico_features(mc: list) -> dict :
    def lexical(mot, fts, idx) :
        for span in chain.from_iterable([(-i, i) for i in range(1, 3 + 1)]):
            if span < 0 :
                if len(mot) >= abs(span) :
                    fts.add("w" + str(idx) + "_pref" + str(abs(span)) + "=" + mot[:-span])
                else :
                    fts.add("w" + str(idx) + "_pref" + str(abs(span)) + "=" + "HayDara")
            else :
                if len(mot) >= abs(span) :
                    fts.add("w" + str(idx) + "_suff" + str(abs(span)) + "=" + mot[-span:])
                else :
                    fts.add("w" + str(idx) + "_suff" + str(abs(span)) + "=" + "HayDara")
        try :
            fts.add("w"+ str(idx) + "_maj=" + str(mot[0].isupper()))
        except :
            pass
        fts.add("w_" + str(idx) + "=" + mot)
        fts.add("w" + str(idx) + "_Maj=" + str(mot.isupper()))

    fts = set()
    lexical(mc[1], fts, 0)

    try :
      fts.add("w_-1=" + mc[0])
      lexical(mc[0], fts, -1)
    except IndexError :
      pass

    try :
      fts.add("w_1=" + mc[2])
      lexical(mc[2], fts, 1)
    except IndexError :
      pass

    return fts


B = 0
I = 1
N = 2

ma = 12.792342964890805
mi = -12.792342964890931

def normalize(val, max, min) : return (val - min) / (max - min)

def score(entree, w) :
  entree = {f : 1 for f in entree}
  score_i = sum(entree[ft] * w[str(I)][ft] for ft in entree if ft in w[str(I)])
  score_n = sum(entree[ft] * w[str(N)][ft] for ft in entree if ft in w[str(N)])

  return round(normalize(score_i, ma, mi), 3), round(normalize(score_n, ma, mi), 3)
