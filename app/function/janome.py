from janome.tokenizer import Tokenizer
import collections

def janome_kaiseki(string,hinsi):
    t = Tokenizer()
    if not hinsi:
        return list(t.tokenize(string,wakati=True))
    return [token.surface for token in t.tokenize(string)if token.part_of_speech.startswith(hinsi)]
          

def calc_frequency_word(string):
    t = Tokenizer()
    s = string
    c = collections.Counter(t.tokenize(s, wakati=True))
    return dict(c)
