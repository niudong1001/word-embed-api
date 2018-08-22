# -*- coding=utf-8 -*-
import urllib.request
import json

baseurl = "http://127.0.0.1:5555/word2vec/"


def fetch_model(word):
    url = baseurl + "model?word="+urllib.parse.quote(word)
    req = urllib.request.urlopen(url)
    res = json.loads(req.read())
    if isinstance(res, str):
        res = list(map(float, res[1:-1].split(",")))
    return res


def fetch_vocab(page_number, page_size=100, shuffle="False"):
    if shuffle not in ["True", "False"]:
        raise BaseException("Shuffle must be a True or False str!")
    url = baseurl + "vocab?page_size="+str(page_size)+"&page_number="+str(page_number)+"&shuffle="+str(shuffle)
    req = urllib.request.urlopen(url)
    res = json.loads(req.read())[1:-1]  # a str, remove "
    res = res.split(" ")
    return res


def fetch_vocab_size():
    url = baseurl + "vocab_size"
    req = urllib.request.urlopen(url)
    res = json.loads(req.read())
    return res


def fetch_most_sim_words(word, topn=5):
    url = baseurl + "similarity?word="+urllib.parse.quote(word)+"&topn="+str(topn)
    req = urllib.request.urlopen(url)
    res = json.loads(req.read())
    return res


def fetch_infer_words(positive_words, negative_words, topn=5):
    pws = ",".join(positive_words)
    nws = ",".join(negative_words)
    url = baseurl + "inference?positive_words="+urllib.parse.quote(pws)+\
          "&negative_words="+urllib.parse.quote(nws)+"&topn="+str(topn)
    req = urllib.request.urlopen(url)
    res = json.loads(req.read())
    return res


if __name__ == "__main__":
    print(fetch_model(word="the"))
    print(fetch_vocab(page_number=0, shuffle="True"))
    print(fetch_vocab_size())
    print(fetch_most_sim_words("the"))
    print(fetch_infer_words(["日", "月"], ["the"]))