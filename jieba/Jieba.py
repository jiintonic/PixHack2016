import jieba
import jieba.analyse
import glob
import re

path = '/Users/albertcheng/Documents/Projects/Pixnet_hackathon_2016/pixnet/'

# Set word_cut dictionary and stopword dictionary
stopwordFile = '/Users/albertcheng/Documents/Projects/20151123_NLP/ch_stopwords.txt'
def get_stopWords(stopwordFile):
    stopWords_set = set()
    content = open(stopwordFile, 'rb').read().decode('utf-8')
    for line in content.splitlines():
        stopWords_set.add(line.strip())
    return stopWords_set
jieba.set_dictionary('/Users/albertcheng/Documents/Projects/20151123_NLP/dict.txt.big.txt')

# Load files from path, and save to dictionary
textfile = {}
for index, doc in enumerate(glob.glob(path+'*.txt')):
    content = open(doc, 'rb').read()
    textfile[index] = []
    for line in content.splitlines():
        line = re.sub('[0-9.]', '', line)
        line = re.sub('www[\w./-]+', '', line)
        line = re.sub('http[:\w./-]+', '', line)
        textfile[index].append(line.strip().decode('utf-8'))
    textfile[index] = ''.join(textfile[index])

# jieba cut!!! and filter stopwords
for index in xrange(len(textfile)):
    seg_words = jieba.cut(textfile[index], cut_all=False, HMM=True)
    words=[]
    stop_sc = get_stopWords(stopwordFile)
    for word in seg_words:
        if word.strip() not in stop_sc:
            words.append(word.strip())
        else:
            pass
    print ' '.join(words)
