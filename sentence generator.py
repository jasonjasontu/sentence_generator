
# Include your imports here, if any are used.
import string
import collections
import random
import math


end = '<END>'
start = '<START>'

def tokenize(text):
    s = ""
    for c in text:
        if c in string.punctuation:
            s += ' %s ' % c;
        else:
            s += c;
    return s.split()

def ngrams(n, tokens):
    result = []
    tokens.append(end)
    for index in xrange(len(tokens)):
        item = ()
        for i in xrange(n-1, 0, -1):
            temp = index - i
            if temp >= 0:
                item += (tokens[temp],)
            else:
                item += (start,)
        result.append((item,tokens[index]))
    return result

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.ngram = {}

    def update(self, sentence):
        for condition, term in ngrams(self.n, tokenize(sentence)):
            if condition in self.ngram:
                self.ngram[condition].append(term)
            else:
                self.ngram[condition] = [term]

    def prob(self, context, token):
        if context in self.ngram:
            c = collections.Counter(self.ngram[context])
            return float(c[token]) / len(self.ngram[context])
        else:return 0

    def random_token(self, context):
        if(len(context) == (self.n-1)):
            index = int(random.random()*len(self.ngram[context]))
            return self.ngram[context][index]
        else:
            print "Function random token requires exactly %d items, but %s is not." %(self.n-1, context)
            return end

    def random_text(self, token_count):
        result = []
        temp = ()
        for i in xrange(self.n-1):
            temp += (start,)
        for i in xrange(token_count-1):
            next_term = self.random_token(temp)
            result.append(next_term)
            temp = ()
            for j in xrange(i-self.n+2, i+1):
                if j < 0:
                    temp += (start,)
                elif result[j] != end:
                    temp += (result[j],)
                else:
                    new_temp = ()
                    for item in temp:
                        new_temp += (start,)
                    temp = new_temp + (start,)
        return ' '.join(result)

    def perplexity(self, sentence):
        token = sentence.split()
        result = 1.0
        token.append(end)

        for i in xrange(len(token)):
            temp = ()
            for j in xrange(i-self.n+1, i):
                if j < 0:
                    temp += (start,)
                else:
                    temp += (token[j],)
            result *= 1.0 / self.prob(temp, token[i])

        return math.pow(result, 1.0/len(token))

def create_ngram_model(n, path):
    model = NgramModel(n)
    f = open(path, 'r')
    for line in f.readlines():
        model.update(line)
    return model

