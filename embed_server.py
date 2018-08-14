# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Resource, Api, reqparse
from gensim.models.word2vec import Word2Vec
import argparse
import json
import numpy as np

parser = reqparse.RequestParser()
app = Flask(__name__)
api = Api(app)


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
            parse.add_argument("word", type=str, required=True, help="Need word for param")
            _args = parse.parse_args()
            word = _args['word']
            print("Query word: "+word)
            if word in model:
                return json.dumps(list(model[word]), cls=MyEncoder)
            else:
                return ""
        except BaseException as e:
            print("Exception of model get: ", e)


class Vocab(Resource):
    def get(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument("page_number", type=int, help="Page number", default=0)
            parse.add_argument("page_size", type=int, help="Page size", default=100)
            _args = parse.parse_args()
            start_index = _args["page_number"]*_args["page_size"]
            _words = words[start_index:start_index+_args["page_size"]]
            _words = " ".join(_words).strip()
            res = json.dumps(_words, ensure_ascii=False)
            # print(res)
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


if __name__ == "__main__":

    global model
    global words
    # parse argument
    p = argparse.ArgumentParser()
    p.add_argument("--model", help="Path to the pre-trained model", required=True)
    p.add_argument("--binary", help="Specifies if the loaded model is binary", default=False)  # can't be wrong!
    p.add_argument("--host", help="Host name", default="localhost")
    p.add_argument("--port", help="Host port", default=5555)
    args = p.parse_args()

    # create model
    model = Word2Vec.load_word2vec_format(args.model, binary=args.binary, unicode_errors='ignore')
    words = model.index2word
    base_url = "/word2vec"
    api.add_resource(Model, base_url+"/model")
    api.add_resource(Vocab, base_url+"/vocab")
    api.add_resource(VocabSize, base_url + "/vocab_size")

    # start web
    app.run(host=args.host, port=args.port, debug=False)  # debug=True
