# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Resource, Api, reqparse
from gensim.models.word2vec import Word2Vec
import argparse
import json
import numpy as np
import random


parser = reqparse.RequestParser()
app = Flask(__name__)
api = Api(app)


def verify_words_exist(words):
    if not isinstance(words, list):
        raise BaseException("Words must be a list!")
    for word in words:
        if word not in model:
            return False, word
    return True, None


def create_error(word):
    return {
            "error": "Word '"+word+"' is not exist in the model!"
        }


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


class Model(Resource):
    def get(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument("word", type=str, required=True, help="Word for query")
            _args = parse.parse_args()
            word = _args['word']
            valid, w = verify_words_exist([word])
            if valid:
                return json.dumps(list(model[word]), cls=MyEncoder)
            else:
                return create_error(w)
        except BaseException as e:
            print("Exception of model get: ", e)


class Vocab(Resource):
    def get(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument("page_number", type=int, help="Page number", default=0)
            parse.add_argument("page_size", type=int, help="Page size", default=100)
            parse.add_argument("shuffle", type=str, help="If shuffle the vocab in every request", default="False")
            _args = parse.parse_args()
            if _args["shuffle"] == "True":
                random.shuffle(words_shuffle)
                __words = words_shuffle
            else:
                __words = words
            start_index = _args["page_number"]*_args["page_size"]
            _words = __words[start_index:start_index+_args["page_size"]]
            _words = " ".join(_words).strip()
            res = json.dumps(_words, ensure_ascii=False)
            return res
        except BaseException as e:
            print("Exception of vocab get: ", e)


class VocabSize(Resource):
    def get(self):
        try:
            size = len(model.index2word)
            return size
        except BaseException as e:
            print("Exception of vocab get: ", e)


class MostSimilar(Resource):
    def get(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument("positive_words", type=str, help="Positive words to query", required=True)
            parse.add_argument("negative_words", type=str, help="Negative words to query")
            parse.add_argument("topn", type=int, help="Get top n similar words", default=5)
            _args = parse.parse_args()
            positive_words = _args["positive_words"].split(",")
            if _args["negative_words"] is not None:
                negative_words = _args["negative_words"].split(",")
            else:
                negative_words = []
            valid, w = verify_words_exist(positive_words+negative_words)
            if valid:
                infers = model.most_similar(positive=positive_words, negative=negative_words, topn=_args["topn"])
                return infers
            else:
                return create_error(w)
        except BaseException as e:
            print("Exception of inference get: ", e)

class Similarity(Resource):
    def get(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument("word_a", type=str, help="Word_a to query", required=True)
            parse.add_argument("word_b", type=str, help="Word_b to query", required=True)
            _args = parse.parse_args()
            word_a = _args["word_a"]
            word_b = _args["word_b"]
            valid, w = verify_words_exist([word_a, word_b])
            if valid:
                sim = model.similarity(word_a, word_b)
                return sim
            else:
                return create_error(w)
        except BaseException as e:
            print("Exception of inference get: ", e)


if __name__ == "__main__":

    global model
    global words
    global words_shuffle

    # parse argument
    p = argparse.ArgumentParser()
    p.add_argument("--model", help="Path to the pre-trained model", required=True)
    p.add_argument("--binary", help="Specifies if the loaded model is binary", default=False)  # can't be wrong!
    p.add_argument("--host", help="Host name", default="localhost")
    p.add_argument("--port", help="Host port", default=5555)
    args = p.parse_args()

    # create model
    print("Loading model...")
    model = Word2Vec.load_word2vec_format(args.model, binary=args.binary, unicode_errors='ignore')
    print("Finished load")

    words = model.index2word
    words_shuffle = words.copy()

    base_url = "/word2vec"
    api.add_resource(Model, base_url+"/model")
    api.add_resource(Vocab, base_url+"/vocab")
    api.add_resource(VocabSize, base_url + "/vocab_size")
    api.add_resource(MostSimilar, base_url + "/most_similar")
    api.add_resource(Similarity, base_url + "/similarity")

    # start web
    app.run(host=args.host, port=args.port, debug=True)  # debug=True
