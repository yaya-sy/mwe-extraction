""" ce module contiendra quelques outils dont aura besoin, \
en particulier ceux qui concernent la lecture des données."""

def get_infos(splite) :
    to_num = {'train':0, 'test':1, 'dev':2}
    infos_split = {}
    for line in splite.split("\n") :
        if line : text, partie = line.split("\t")
        infos_split[text] = to_num[partie]
    return infos_split

def read_corpus(corpus: _io.TextIOWrapper, infos_split: _io.TextIOWrapper):
    """
    Fonction qui lit le corpus en renvoyant un liste pour chaque corpus.
    Pour chaque corpus, on a une liste de tuples (phrase, tags_de_la_phrase)

    Paramaters
    ----------
    - corpus : _io.TextIOWrapper
      le fichier conlu
    - infos_split : _io.TextIOWrapper
      le fichier contenant les informations sur les repartitions
      train, test et dev.
    """
    train_test_dev = [[], [], []]
    for sentence in corpus.read().split("\n\n"):
      if not sentence:
        continue
      data = []
      span = None
      for line in sentence.split("\n") :
        if line.startswith("# sent_id") :
          partie = infos_split[line.split("= ")[1]]
        splits = line.split("\t")[:11] if not line.startswith("#") else None
        if splits :
          indice, word, pos = splits[0], splits[1], splits[3]
          if "-" not in indice and "." not in indice :
            if len(splits[-1]) > 1 and "MWE" in splits[-1]: #pour exclure NE
              span = splits[-1].split(":")[0]
              pos = "B_" + pos
              data.append((word, pos))

            elif span and splits[-1] != "*" :
              pos = "I_" + pos
              data.append((word, pos))

            else :
              pos = "B_" + pos
              data.append((word, pos))

      if data :
        wds, pos = zip(*((w, pos) for w, pos in data))
        train_test_dev[partie].append([wds, pos])
    return train_test_dev
