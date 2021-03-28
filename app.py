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
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        contentData = request.get_json()
        url = "https://optimusbt.azurewebsites.net/api/Bug/GetUSERecord/" + contentData['project_name'] + "/" + \
              contentData['component_name']
        response = req.get(url, verify=False)
        data = pd.DataFrame(response.json())
        my_list = []
        summary = data['summary'].values
        for sent in data.index:
            filtered_sentence = remove_stopwords(data.at[sent, 'summary'])
            data.loc[sent, 'Keywords'] = filtered_sentence
        module_url = "universal-sentence-encoder_4"
        model = hub.load(module_url)
        summary = data['Keywords'].values
        sentence_embeddings = model(summary)
        d = data.to_json(orient='records')
        jsonData = json.loads(d)
        return jsonify(jsonData)
    else:
        return "Working Python Get"