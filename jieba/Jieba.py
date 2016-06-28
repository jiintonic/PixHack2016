import jieba
import jieba.analyse
import glob
import re
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


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

# Load files from path, and save to text file
fileName = path+'test/test.txt'

with open(fileName, 'w+') as f:
    # Read article one by one, memory friendly
    for doc in glob.glob(path+'*.txt'):
        # tmp: save content without new line, http
        tmp = []
        content = open(doc, 'rb').read()
        for line in content.splitlines():
            line = re.sub('[0-9.]', '', line)
            line = re.sub('www[\w./-_]+', '', line)
            line = re.sub('http[:\w./-_]+', '', line)
            tmp.append(line.strip())
        tmp = ''.join(tmp)
        seg_words = jieba.cut(tmp, cut_all=False, HMM=True)
        # words: save content after jieba and remove stop words, words separate by blank
        words = []
        stop_sc = get_stopWords(stopwordFile)
        for word in seg_words:
            if word.strip() not in stop_sc:
                words.append(word.strip().encode('utf-8'))
            else:
                pass
        words[0]
        f.write(re.sub('\s+', ' ', ' '.join(words))+'\n')
    f.close()