# Word Embedding Api

## Dependency

```bash
Flask==0.10.1
Flask-RESTful==0.2.12
gensim==0.12.3
```

## Usage

1. Start server：
   - Use `vec`: `python embed_server.py --model ./data/wiki.zh.test.vec`
   - Use `bin`: `python embed_server.py --model *.bin --binary`

 > change to your own *.vec or *.bin file

2. Get embed data:

```python
from embed_api import fetch_model, fetch_vocab, fetch_vocab_size, fetch_most_sim_words, fetch_infer_words, fetch_similarity
print(fetch_model(word="name"))  # [-0.014032557606697083, -0.01409541629254818,...]
print(fetch_vocab(page_number=0, page_size=100))  # ['</s>', '，', '的', ...]
print(fetch_vocab_size())  # 99
print(fetch_most_sim_words(word="the"))  # [['a', 0.8761178255081177], ['e', 0.8689581751823425], ...]
print(fetch_infer_words(positive_words=["日", "月"], negative_words=["上"]))  # [['年', 0.8870731592178345], ...]
print(fetch_similarity(word_a="a", word_b="the"))  # 0.8761178251873356
```
