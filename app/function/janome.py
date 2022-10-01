from janome.tokenizer import Tokenizer
import collections

def janome_kaiseki(string):
    t = Tokenizer()
    s = string
    return [token.surface for token in t.tokenize(s)if token.part_of_speech.startswith('名詞')]

def test(string):
    t = Tokenizer()
    s = string
    c = collections.Counter(t.tokenize(s, wakati=True))
    return dict(c)
