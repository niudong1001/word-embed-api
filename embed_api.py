# -*- coding=utf-8 -*-
import urllib.request
import json

baseurl = "http://127.0.0.1:5555/word2vec/"


def fetch_model(word):
    url = baseurl + "model?word="+urllib.parse.quote(word)
    req = urllib.request.urlopen(url)
    res = json.loads(req.read())
    if len(res) <= 5:
        return "-1"
    res = list(map(float, res[1:-1].split(",")))
    return res


def fetch_vocab(page_number, page_size=100, shuffle="False"):
    url = baseurl + "vocab?page_size="+str(page_size)+"&page_number="+str(page_number)+"&shuffle="+str(shuffle)
    req = urllib.request.urlopen(url)
    res = json.loads(req.read())[1:-1]  # a str, remove "
    # print(type(res))
    res = res.split(" ")
    return res


def fetch_vocab_size():
    url = baseurl + "vocab_size"
    req = urllib.request.urlopen(url)
    res = json.loads(req.read())
    return res


if __name__ == "__main__":
    print(fetch_model(word="the"))
    print(fetch_vocab(page_number=0, shuffle="False"))
    print(fetch_vocab_size())