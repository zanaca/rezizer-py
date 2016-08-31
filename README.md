# RezizerUrl - a Python Rezizer Url Generator

## Install

run:
```python
pip install rezizer-url
```

## Usage

```python
import rezizer

secret_key = 'OhMyG0shWhatASecretKey!'

# start the generator
rezizerGenerator = rezizer.rezizerUrl('http://your.rezizer.url:port', secret_key)

# get the Rezized url
imageUrl = rezizerGenerator.withUrl('http://your.domain.url/foo/bar.jpg').resize(100, 100).generate()
```
