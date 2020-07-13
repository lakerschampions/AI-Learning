# 获取推特数据并用PDA主题聚类进行数据分析的python简单实现
## 相关知识
- python tweepy库（用来获取推特数据）
- python nltk库（在规范数据时会用到）
- python pandas库（将数据存放进矩阵中便于分析）

```
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re
import string
import gensim
from gensim import corpora
import tweepy
import time
import pandas as pd
import numpy as np
import requests
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
```

## 1.连接api
consumer_key = 'XXXXXXXXX'
consumer_secret = 'XXXXXXXX'
access_token = 'XXXXXXXX'
access_token_secret = 'XXXXXXXX'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  #排除速率限制带来的干扰

## 2.获取hashtag为“COVID19”的10000条tweets
抓取具有特定hashtag的10000条最新的tweets，规定语言为英语
```
CovidList = []
i = 10000
t1 = time.time()

tweets = api.search(q='COVID19',lang='en',tweet_mode='extended',count=i)

# print(dir(tweets[0]))

for tweet in tweets:
# 有些tweets是转发他人的，所以需要获取转发的tweets的fulltext
    if 'retweeted_status' in dir(tweet):
        CovidList.append(tweet.retweeted_status.full_text)
    else:
        CovidList.append(tweet.full_text)  

t2 = time.time()

print("获取",i,"条tweets耗时",t2-t1,'s')
```
获取的tweets文本被存放在了CovidList中，预计输出类似<em>"获取 10000 条tweets耗时 11.249251127243042 s"</em>。

## 3.规范数据
从nltk导入stopwords库，从string导入punctuation，去除了tweets中的停用词（对文本影响不大但是经常出现的没有意义的词，诸如it，is，a，an等）和标点符号。用<em>WordNetLemmatizer</em>将词语规范化（类似eating会被转化成eat）
```
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(sentence):
    stop_free = " ".join([i for i in sentence.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

CleanList = [clean(sen).split() for sen in CovidList]
```

有些词语会在转化的过程中自动产生（比如amp），由于我们是希望在跟covid19相关的tweets中获取他们的主题，所以我们也不希望covid19出现在结果里，所以我在这里把他们放进remove_list里删除，具体的list可以在后期继续补充
```
remove_list = ['amp','&amp','#covid19','covid19','u']
for tweet in CleanList:
    for word in tweet:
        if word in remove_list:
            tweet.remove(word)
```

## 4.建立模型，并进行训练
建立两个主题聚类的模型
```
dictionary = corpora.Dictionary(CleanList)
corpus = [dictionary.doc2bow(tweet) for tweet in CleanList]
t3 = time.time()
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(corpus, num_topics=2, id2word = dictionary, passes=50)
t4 = time.time()
print("训练",i,"条tweets耗时",t4-t3,'s')
```

## 5.输出结果
两个主题聚类，每个主题四个关键词
```
print(ldamodel.print_topics(num_topics=2,num_words=4))
```
最后的结果：<em>[(0, '0.007*"mask" + 0.005*"join" + 0.005*"help" + 0.005*"challenge"'), (1, '0.008*"death" + 0.007*"patient" + 0.005*"positive" + 0.005*"blood"')]</em><br>

## 6.总结
可以发现，第一个主题的四个关键词是mask，join，help，challenge，我们或许可以根据这四个单词联想到，人们获取口罩是一种挑战或是口罩帮助人们客服挑战之类；而第二个主题与death,patient,blood有关，显然这与医院中的救援相关；这些就是我们从用户的tweets中获取的主题。
