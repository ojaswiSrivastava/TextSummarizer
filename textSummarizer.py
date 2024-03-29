import numpy as np
import pandas as pd
import nltk

nltk.download('punkt')

# Read the Data
df = pd.read_csv('tennis_articles_v4.csv')
df
df['article_text'][0]
df['article_text'][1]

# Split Text into Sentences
from nltk.tokenize import sent_tokenize

sentences = []
for s in df['article_text']:
    sentences.append(sent_tokenize(s))

sentences = [y for x in sentences for y in x]
print(sentences[:5])

# Text Preprocessing
clean_sentences = pd.Series(sentences).str.replace('[^a-zA-Z]','')
clean_sentences = [s.lower() for s in clean_sentences]

nltk.download('stopwords')

from nltk.corpus import stopwords

stop_words = stopwords.words('english')

#function to remove stopwords
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

# remove stopwords from the sentences
clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

# Extract word vectors
word_embeddings = {}
f = open('glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

# Vector Representation of Sentences
sentence_vectors = []
for i in clean_sentences:
    if len(i) != 0:
        v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
    else:
        v = np.zeros((100,))
    sentence_vectors.append(v)

# Similarity Matrix Preparation
sim_mat = np.zeros([len(sentences), len(sentences)])

from sklearn.metrics.pairwise import cosine_similarity

for i in range(len(sentences)):
    for j in range(len(sentences)):
        if i != j:
            sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100),sentence_vectors[j].reshape(1,100))[0,0]

# Applying PageRank Algorithm
import networkx as nx

nx_graph = nx.from_numpy_array(sim_mat)
scores = nx.pagerank(nx_graph)

ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

# Summary Extraction
# Extract top 10 sentences as the summary
for i in range(10):
    print(ranked_sentences[i][1])