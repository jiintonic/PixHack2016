#encoding=utf-8
#!/usr/bin/python
import gensim, logging
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Set features
dirnamecsvFile='test.txt'
model_name='Pixnet2016'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            content = open(self.dirname+fname, 'rb').read()
            for line in content.splitlines():
                yield line.split()

def trainModelByfile():
    sentences = MySentences('scrapy_wiki/') # a memory-friendly iterator
    model = gensim.models.Word2Vec(sentences)
    return model

def saveModel(trainModel,modelName):
    trainModel.save(modelName)

def loadModel(modelName):
    new_model = gensim.models.Word2Vec.load(modelName)
    return new_model

def usingModel(model):
    similarity = raw_input("Input word:")
    print('most_similar:' +similarity)
    for w in model.most_similar(similarity, topn=5):
       print w[0], w[1]

def fromArticleFile():
    sentences = MySentences('scrapy_wiki/') # a memory-friendly iterator
    model = gensim.models.word2vec.Word2Vec(sentences, size=200, window=8, min_count=1, sample=0.001,\
                                            sg=0, hs=1, negative=0, cbow_mean=1, workers=3, iter=3)
    saveModel(model, model_name)

def fromSavedModel():
    new_model = gensim.models.Word2Vec.load(model_name)
    usingModel(new_model)


# fromArticleFile()
fromSavedModel()