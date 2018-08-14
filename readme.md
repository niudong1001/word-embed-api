# Word Embedding Api

## Usage

1. Start server：
   - Use `vec`: `python embed_server.py --model ./data/wiki.zh.test.vec`
   - Use `bin`: `python embed_server.py --model *.bin --binary`
2. Get embed data:
```python
from embed_api import fetch_model, fetch_vocab, fetch_vocab_size
print(fetch_model(word="name"))  # [-0.014032557606697083, -0.01409541629254818,...]
print(fetch_vocab(page_number=0, page_size=100))  # ['</s>', '，', '的', ...]
print(fetch_vocab_size())  # 99
```
