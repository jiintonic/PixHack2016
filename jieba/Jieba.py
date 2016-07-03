#!/usr/bin/env python
import jieba
import jieba.analyse
import glob
import re
import codecs
import sys
import os
from lib.pixnetdb import PixnetDB

reload(sys)
sys.setdefaultencoding('utf-8')

currentPath = os.path.dirname(os.path.realpath(__file__))

# Set word_cut dictionary and stopword dictionary
stopwordFile = 'ch_stopwords.txt'
stopwordFilePath = os.path.join(currentPath, 'dict', stopwordFile)
dictFile = 'dict.txt.big.txt'
dictFilePath = os.path.join(currentPath, 'dict', dictFile)
jieba.set_dictionary(dictFilePath)

def get_stopWords(stopwordFile):
    stopWords_set = set()
    content = open(stopwordFile, 'rb').read().decode('utf-8')
    for line in content.splitlines():
        stopWords_set.add(line.strip())
    return stopWords_set

# Load articles from pixnetdb
def load_data():
    db = PixnetDB()
    data_tuple = db.get_articles()
    data_list = []
    for data in data_tuple:
        data_list.append(data[0])
    return data_list

def filter_words(content):
    tmp = []
    for line in content.splitlines():
        line = re.sub('[0-9.]', '', line)
        line = re.sub('www[\w./-_]+', '', line)
        line = re.sub('http[:\w./-_]+', '', line)
        tmp.append(line.strip())
    return tmp

def write_file(content):
    fileName = os.path.join(currentPath, 'test.txt')
    with open(fileName, 'a+') as f:
        f.write(content)

def start_jieba(data):
    for content in data:
        tmp = ''.join(filter_words(content))
        seg_words = jieba.cut(tmp, cut_all=False, HMM=True)
        # words: save content after jieba and remove stop words, words separate by blank
        words = []
        stop_sc = get_stopWords(stopwordFilePath)
        for word in seg_words:
            if word.strip() not in stop_sc:
                words.append(word.strip().encode('utf-8'))
            else:
                pass
        write_file(re.sub('\s+', ' ', ' '.join(words))+'\n')

def main():
    articles = load_data()
    start_jieba(articles)


if __name__ == '__main__':
    main()
