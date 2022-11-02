from crypt import methods
import os
import flask
import index
import pathlib
import re
import collections
import math

@index.app.before_first_request
def startup():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    read_stopwords(index_dir)
    read_pagerank(index_dir)
    read_inverted_index(index_dir)

def read_stopwords(dir):
    file = os.path.join(dir, 'stopwords.txt')
    index.app.config['STOP_WORDS'] = set([line.rstrip('\n') for line in open(file)])

def read_pagerank(dir):
    file = os.path.join(dir, 'pagerank.out')
    lines = [line.strip().split(',') for line in open(file)]
    index.app.config['PAGE_RANK'] = {int(line[0]): float(line[1]) for line in lines}

def read_inverted_index(dir):
    file = os.path.join(dir, 'inverted_index', index.app.config['INDEX_PATH'])
    lines = [line.strip().split() for line in open(file)]
    index.app.config['INVERTED_INDEX'] = {
        line[0]: {
            'idf': float(line[1]), 
            'doc': split_doc_line(line[2:])
        } 
        for line in lines
    }

def split_doc_line(line):
    res = {}
    for i in range(0, len(line), 3):
        res[int(line[i])] = {'tf': int(line[i+1]), 'norm': float(line[i+2])}
    return res

@index.app.route('/api/v1/', methods = ['GET'])
def get_v1():
    context = {
        'hits': '/api/v1/hits/',
        'url': '/api/v1/'
    }
    return flask.jsonify(**context), 200

@index.app.route('/api/v1/hits/', methods = ['GET'])
def get_hits():
    query = flask.request.args.get('q', default='', type=str)
    if query == '':
        context = {'hits': []}
        return flask.jsonify(**context), 200
    
    # clean the query
    query = query.replace('+', ' ')
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    
    weight = flask.request.args.get('w', default=0.5, type=float)
    
    words = [q for q in query.split() if q not in index.app.config['STOP_WORDS']]
    word_count = collections.Counter(words)
    
    # filter docs containing words
    docs = filter_docs(word_count)
    if docs == []:
        context = {'hits': []}
        return flask.jsonify(**context), 200
    
    # calculate tfidf
    tfidf = calculate_tf_idf(word_count, docs)
    
    # get pagerank
    page_rank = index.app.config['PAGE_RANK']
    
    # calculate score
    score = [(item[0], item[1]*(1-weight) + page_rank[item[0]]*weight) for item in tfidf]
    score.sort(key=lambda x: x[1], reverse=True)
    
    context = {'hits': [{'docid': s[0], 'score': s[1]} for s in score]}
    return flask.jsonify(**context), 200



def filter_docs(word_count):
    inverted_index = index.app.config['INVERTED_INDEX']
    docs = set()
    for word in word_count.keys():
        if word not in inverted_index:
            return []
        if len(docs) == 0:
            docs = set(inverted_index[word]['doc'].keys())
        else:
            docs = docs.intersection(inverted_index[word]['doc'].keys())
    return docs


def calculate_tf_idf(word_count, docs):
    inverted_index = index.app.config['INVERTED_INDEX']
    
    q_vec = [inverted_index[word]['idf']*count for word, count in word_count.items()]
    q_norm = math.sqrt(sum([q**2 for q in q_vec]))
    
    res = []
    for doc in docs:
        d_vec = [inverted_index[word]['idf']*inverted_index[word]['doc'][doc]['tf'] for word in word_count.keys()]
        d_norm = math.sqrt(inverted_index[list(word_count.keys())[0]]['doc'][doc]['norm'])
        tfidf = sum([q*d for q, d in zip(q_vec, d_vec)])/(q_norm*d_norm)
        res.append((doc, tfidf))
    
    return res