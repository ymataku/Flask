from janome.tokenizer import Tokenizer
def janome_kaiseki(string):
    t = Tokenizer()
    s = string
    return [token.surface for token in t.tokenize(s)if token.part_of_speech.startswith('名詞')]