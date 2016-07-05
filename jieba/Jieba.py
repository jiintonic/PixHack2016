#!/usr/bin/env python
import jieba
import jieba.analyse
import glob
import re
import codecs
import sys
import os
import threading
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
        line = re.sub('[\w./-_@]+com', line)
        tmp.append(line.strip())
    return tmp

def write_file(content, fileName):
    with open(fileName, 'a+') as f:
        f.write(content)

def start_jieba(data, fileName):
    f =  open(os.path.join(currentPath, fileName), 'a+')
    for content in data:
        tmp = ''.join(filter_words(content))
        tmp = tmp.lower()
        seg_words = jieba.cut(tmp, cut_all=False, HMM=True)
        # words: save content after jieba and remove stop words, words separate by blank
        words = []
        stop_sc = get_stopWords(stopwordFilePath)
        for word in seg_words:
            if word.strip() not in stop_sc:
                words.append(word.strip().encode('utf-8'))
            else:
                pass
        f.write(re.sub('\s+', ' ', ' '.join(words))+'\n')
    f.close()

def partition_data(data, number):
    if len(data) < number:
        return [data]

    n = len(data) / number
    part_data = []
    for i in range(number-1):
        p = data[n*i: n*(i+1)]
        part_data.append(p)

    t = data[n*(number-1):]
    part_data.append(t)
    return part_data

class JiebaThread(threading.Thread):
    # Override run funciton
    def __init__(self, data, fileName, threadName):
        super(JiebaThread, self).__init__(name = threadName)
        self.data = data
        self.fileName = fileName

    def run(self):
        start_jieba(self.data, self.fileName)

def start_jieba_thread(data, num):
    # use 4 threads
    pdata = partition_data(data, num)
    th = []
    for i in range(num):
        print "Thread %d" % (i)
        fileName = 'test%d.txt' % (i)
        threadName = 'thread%d' % (i)
        t = JiebaThread(pdata[i], fileName, threadName)
        t.start()
        th.append(t)

    for t in th:
        t.join()

def main():
    articles = load_data()

    # We need thread to process massive articles
    if len(articles) > 100:
        start_jieba_thread(articles, 4)
    else:
        start_jieba(articles, 'test.txt')


if __name__ == '__main__':
    main()
