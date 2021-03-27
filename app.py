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
@app.route('/<project_name>')
def home(project_name):
     return project_name
