#!/usr/bin/env python

import json
import logging

import qnd
import qndex
import font2char2word2sent2doc


model = font2char2word2sent2doc.def_font2char2word2sent2doc()
read_file = qndex.nlp.sentiment_analysis.def_read_file()
infer = qnd.def_infer()


def main():
    logging.getLogger().setLevel(logging.INFO)
    print(json.dumps(next(infer(model, read_file))['font_attentions']
                     .tolist()))


if __name__ == "__main__":
    main()
