#!/usr/bin/env python

import logging

import qnd
import qndex
import font2char2word2sent2doc


model = font2char2word2sent2doc.def_font2char2word2sent2doc()
read_file = qndex.nlp.sentiment_analysis.def_read_file()
train_and_evaluate = qnd.def_train_and_evaluate()


def main():
    logging.getLogger().setLevel(logging.INFO)
    train_and_evaluate(model, read_file)


if __name__ == '__main__':
    main()
