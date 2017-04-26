#!/usr/bin/env python

import logging

import qnd
import qndex
import font2char2word2sent2doc


model = font2char2word2sent2doc.def_font2char2word2sent2doc()
read_file = qndex.nlp.sentiment_analysis.def_read_file()
evaluate = qnd.def_evaluate()


def main():
    logging.getLogger().setLevel(logging.INFO)
    print(evaluate(model, read_file))


if __name__ == '__main__':
    main()
