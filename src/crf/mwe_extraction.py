from evaluation import *
from features import *
from utils import *

from itertools import chain
import random

import sklearn_crfsuite


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus',
        required=True,
        help='le corpus conlu parseme'
        )

    parser.add_argument('--split_infos',
        required=True,
        help='les informations de split dev, test, train'
        )

    args = parser.parse_args()
    corpus = open(args.corpus)
    infos_split = get_infos(open(args.split_infos, "r").read())

    train, test, dev = read_corpus(corpus, infos_split)

    feats = Features(train, test, dev, 4, 1)
    train, test, dev = feats.get_features()
    train_feats, train_golds = train
    test_feats, test_golds = test
    dev_feats, dev_golds = dev

    crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    max_iterations=1000,
    c1=0.1258223157965275,
    c2=0.008765058107413456,
    all_possible_transitions=True
    )

    crf.fit(train_feats, train_golds)

    evaluation = Evaluation(crf, test_golds, test_feats, train_feats, train_golds)

    print("precision oov : ", evaluation.precision_oov())
    print("precision sur les mots composés : ", evaluation.b_i_precision())
    print("fscore sur les mots composés : ", evaluation.fscore())
