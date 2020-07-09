import nltk
from nltk.corpus import brown
import re
from nltk.stem import WordNetLemmatizer as WL
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
from nltk import FreqDist
from nltk.text import TextCollection

emotions_str = r"""
    (?:
        [:=;] # 眼睛
        [oO\-]? # ⿐鼻⼦子
        [D\)\]\(\]/\\OpP] # 嘴
    )"""
regex_str = [
    emotions_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @某⼈人
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # 话题标签
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # 数字
    r"(?:[a-z][a-z'\-_]+[a-z])",  # 含有 - 和 ‘ 的单词
    r'(?:[\w_]+)',  # 其他
    r'(?:\S)'  # 其他
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)  # 所有特殊字符的匹配式
emotion_re = re.compile(r'^' + emotions_str + '$', re.VERBOSE | re.IGNORECASE)  # 表情符号的匹配式


def tokenize(s):
    return tokens_re.findall(s)  # 匹配出所有特殊字符


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emotion_re.search(token) else token.lower() for token in tokens]  # 对非表情符号进行小写处理
    return tokens  # 返回所有特殊字符


sentence = "RT @DesireeAngelll: Testing positive for COVID-19 is ok but what\xe2\x80\x99s NOT ok is going around " \
           "acting like you don\xe2\x80\x99t have it and endangering eve\xe2\x80\xa6. "
tokens = preprocess(sentence)
# print(tokens)

wl = WL()
# print(wl.lemmatize('is'), wl.lemmatize('is', pos='v'))

filtered_words = [word for word in tokens if word not in stopwords.words('english')]
# print(filtered_words)

sentiment_dictionary = {}
for line in open('AFINN-111.txt'):
    word, score = line.split('\t')
    sentiment_dictionary[word] = int(score)

total_score = sum(sentiment_dictionary.get(word, 0) for word in tokens)
# print(total_score)

s1 = 'this is a good book'
s2 = 'this is a awesome book'
s3 = 'this is a bad book'
s4 = 'this is a terrible book'


def proprocess(s):
    return {word: True for word in s.lower().split()}


training_data = [[proprocess(s1), 'pos'],
                 [proprocess(s2), 'pos'],
                 [proprocess(s3), 'neg'],
                 [proprocess(s4), 'neg']]

model = NaiveBayesClassifier.train(training_data)


# print(model.classify(proprocess('this is a good shook')))


def proprocess2(s):
    tokens2 = preprocess(s)
    filterer_words2 = [word for word in tokens2 if word not in stopwords.words('english')]
    pos_tag = nltk.pos_tag(filterer_words2)
    return {i[0]: i[1] for i in pos_tag}


proprocess2('this is a good book')

corpus = 'this is my sentence ' \
         'this is my life ' \
         'this is the day'

tokens = nltk.word_tokenize(corpus)
fdist = FreqDist(tokens)
standard_freq_vector = fdist.most_common(50)
size = len(standard_freq_vector)


print(standard_freq_vector)

def position_lookup(v):
    res = {}
    counter = 0
    for word in v:
        res[word[0]] = counter
        counter += 1
    return res


standard_position_dict = position_lookup(standard_freq_vector)
# print(standard_position_dict)

sentence = 'this is cool'
freq_vector = [0] * size
tokens = nltk.word_tokenize(sentence)
for word in tokens:
    try:
        freq_vector[standard_position_dict[word]] += 1
    except KeyError:
        continue

# print(freq_vector)

corpus = TextCollection(['this is sentence one',
                         'this is sentence two',
                         'this is sentence three'])

standard_vocab = []
for i in standard_freq_vector:
    standard_vocab.append(i[0])

# print(corpus.tf('is', 'this is sentence four'))

new_sentence = 'this is sentence five'
for word in standard_vocab:
    print(corpus.tf_idf(word, new_sentence))

