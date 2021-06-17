"""Ce module module contient des fonction d'extraction de caractéristiques pour la baseline
"""
from itertools import chain
def features(phrase, tags, span_w, span_s, position) :
    """
    Fonction qui extrait les features en créant un dictionnaire : pour chaque mot (par exemeple 'désinfection'), on regarde
        - pref1 (son préfixe de longueur 1) : 'd'
        - pref2 (son préfixe de longueur 2) : 'dé'
        - etc
        - suff1 (son suffixe de longueur 1) : 'n'
        - suff2 (son suffixe de longueur 2) : 'on'
        - suff3 (son suffixe de longueur 3) : 'ion'
        - etc.
    """
    beg, end = list(zip(*((f"@BEG{i}@", f"@END{i}@")  for i in range(span_s))))
    beg, end = list(beg), list(end)
    span_s += 1
    l = len(phrase)
    p = beg + phrase + end
    t = beg + tags + beg
    features = []
    if p[position] not in beg + end : #and mot in mc and mot not in mots :
        for spann in chain.from_iterable([(-i, i) for i in range(1, span_s)]) :
            features.append("w_" + str(spann) + " = " + p[position + spann])
            if spann < 0 : features.append("t_" + str(spann) + " = " + t[position + spann])

        for span in chain.from_iterable([(-i, i) for i in range(1, span_w + 1)]):
            if span < 0 :
                if len(p[position]) >= abs(span) :
                    features.append("pref" + str(abs(span)) + "=" + p[position][:-span])
                else :
                    features.append("pref" + str(abs(span)) + "=" + "HayDara")
            else :
                if len(p[position]) >= abs(span) :
                    features.append("suff" + str(span) + "=" + p[position][-span:])
                else :
                    features.append("suff" + str(abs(span))  + "=HayDara")

        features.append("maj" + "=" + str(p[position][0].isupper()))
        features.append("mot" + "=" + p[position])
        features.append("Maj" + "=" + str(p[position].isupper()))
    if bool(features) :
        return features, t[position]

def get_features(corpus) :
    """
    fonction qui parcourt les phrase pour extraire les caractéristiques

    Returns
    -------
    - tuple :
      les caractéristiques et les classes
    """
    fts = []
    golds = []
    for phrase, labels in corpus :
        if len(phrase) <= 1:continue
        for i in range(len(phrase)) :
          f = features(list(phrase), list(labels), 4, 1, i)
          if f != None :
            f,g = f
            fts.append(f)
            golds.append(g)

    return fts, golds
