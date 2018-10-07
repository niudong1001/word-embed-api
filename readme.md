# Word-Embed-Api

Fetch word embedding data like `word2vec` from a web server.  

## Dependency

```bash
Python3+
Flask==0.10.1
Flask-RESTful==0.2.12
gensim==0.12.3
```
You can use `pip install -r requirements.txt` to install all dependency.

## Usage

1. Start a server:

- Use `vec` data: `python embed_server.py --model ./data/wiki.zh.test.vec`
- Use `bin` data: `python embed_server.py --model *.bin --binary`

 > Please change to your own `*.vec` or `*.bin` file.

2. Fetch embed data by python:

```python
from embed_api import fetch_model, fetch_vocab, fetch_vocab_size, fetch_most_sim_words, fetch_infer_words, fetch_similarity

print(fetch_model(word="name"))  # [-0.014032557606697083, -0.01409541629254818,...]
print(fetch_vocab(page_number=0, page_size=100))  # ['</s>', '，', '的', ...]
print(fetch_vocab_size())  # 99
print(fetch_most_sim_words(word="the"))  # [['a', 0.8761178255081177], ['e', 0.8689581751823425], ...]
print(fetch_infer_words(positive_words=["日", "月"], negative_words=["上"]))  # [['年', 0.8870731592178345], ...]
print(fetch_similarity(word_a="a", word_b="the"))  # 0.8761178251873356
```
> you can use `test_api.py` to test.

3. Fetch embed data by curl:
```bash
curl http://127.0.0.1:5555/word2vec/model?word=the
curl http://127.0.0.1:5555/word2vec/vocab?page_number=0&page_size=50&shuffle=False
curl http://127.0.0.1:5555/word2vec/vocab_size
curl http://127.0.0.1:5555/word2vec/most_similar?positive_words=the,a&negative_words=an&topn=5
curl http://127.0.0.1:5555/word2vec/similarity?word_a=the&word_b=a
```

## References

- https://github.com/3Top/word2vec-api