from pytest import param
import requests
import search
import flask
import threading

hits_lock = threading.Lock()



@search.app.route('/search/', methods=['GET'])
def search_res():
    conn = search.model.get_db()
    query = flask.request.args.get('q')
    weight = flask.request.args.get('w')
    if weight is None:
        weight = 0.5
    if query is None:
        query = ''
        context = {
            'q': query,
            'w': weight,
            'hits': [],
            'num_hits': 0
        }
        return flask.render_template('index.html', **context)
    
    hits = []
    threads = []
    for index_server in search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']:
        index_thread = threading.Thread(
            target=get_index_server, 
            args=(index_server, {'q': query, 'w': weight}, hits)
        )
        threads.append(index_thread)
        index_thread.start()
    
    # pause the main thread
    for t in threads:
        t.join()
    
    hits.sort(key=lambda x: x['score'], reverse=True)
    documents = []
    for h in hits[:min(10, len(hits))]:
        cur = conn.execute('''
            SELECT title, url, summary
            FROM DOCUMENTS 
            WHERE docid = ?
        ''', (h['docid'], ))
        doc = cur.fetchone()
        documents.append({
            'docid': h['docid'],
            'title': doc[0],
            'url': doc[1],
            'summary': doc[2]
        })
    context = {'q': query, 'w': weight, 'hits': documents, 'num_hits': len(documents)}
    return flask.render_template('index.html', **context)
    

def get_index_server(url, params, hits):
    response = requests.get(url=url, params=params)
    hits_lock.acquire()
    hits += response.json().get('hits', [])
    hits_lock.release()

