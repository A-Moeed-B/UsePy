from flask import Flask, request,jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import requests as req
import json
from gensim.parsing.preprocessing import remove_stopwords

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/usepy/', methods=['GET', 'POST'])
def query_example():
    contentData=request.get_json()
    url="https://localhost:44300/api/Bug/GetUSERecord/"+contentData['project_name']+"/"+contentData['component_name']
    response=req.get(url,verify=False)
    data=pd.DataFrame(response.json())
    my_list = []
    summary = data['summary'].values
    for sent in data.index:
        filtered_sentence = remove_stopwords(data.at[sent, 'summary'])
        data.loc[sent, 'Keywords'] = filtered_sentence

    module_url = "universal-sentence-encoder_4" 
    model = hub.load(module_url)

    summary = data['Keywords'].values
    sentence_embeddings = model(summary)

    query = contentData['summary']
    query_sentence = remove_stopwords(query)
    query_vec = model([query_sentence])[0]

    def cosine(u, v):
        return (np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))*100


    similarity = []
    for  sent in data.index:
      sim = cosine(query_vec, model([data.at[sent,'Keywords']])[0])
      data.loc[sent, 'Similarity'] = sim

    datanew=data.loc[(data['Similarity'] >= 30)]

    datanew=datanew.sort_values(by='Similarity', ascending=False)
    topTen=datanew.head(10)

    d=topTen.to_json(orient='records')
    jsonData=json.loads(d)
    return jsonify(jsonData)
    #return contentData['project_name']+" "+contentData['component_name']+" "+contentData['summary']

if __name__ == '__main__':
    app.run(debug=True, port=5000)