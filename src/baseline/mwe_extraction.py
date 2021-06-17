from evaluation import *
from features import *
from utils import *

from collections import Counter, defaultdict
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from itertools import chain
import random

from sklearn.linear_model import LogisticRegression


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

    train_feats, train_golds = get_features(train)
    test_feats, test_golds = get_features(test)
    dev_feats, dev_golds = get_features(dev)

    vectorizer = CountVectorizer(analyzer=lambda x: x)
    X_train = vectorizer.fit_transform(train_feats)
    X_test = vectorizer.transform(test_feats)
    X_dev = vectorizer.transform(dev_feats)

    rl = LogisticRegression(solver="sag", max_iter=1000)
    rl.fit(X_train, train_golds)

    eval = Evaluation(rl, test_golds, test_feats, X_test, train_feats, X_train, train_golds)

    print("precision oov : ", eval.precision_oov())
    print("precision sur les mots composés : ", eval.b_i_precision())
    print("fscore sur les mots composés : ", eval.fscore())
