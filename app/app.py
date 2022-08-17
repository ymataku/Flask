from flask import Flask, render_template,request
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
# token = ""
import json
import requests
from greeting import Hello 
import MeCab
# from function import Cotoha 
token = ""
# vec1 = np.array([1,2,3])
app = Flask(__name__)
def ConnectCotoha():
    # https://api.ce-cotoha.com/home の
    # Client ID って書いてあるところにあるやつ
    client_id     = 'PYt5RmFrK9Gprd3g0rOXcRem274cxN3W'
    # Client Secret って書いてあるところにあるやつ
    client_secret = 'YZi4Bs9qUlXy63Gb'

    # Access Token Publish URL って書いてあるところにあるやつ
    url = 'https://api.ce-cotoha.com/v1/oauth/accesstokens'
    # https://api.ce-cotoha.com/contents/reference.html の
    # リファレンスにあるやつ。でも面倒だから書きたくないよね。
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        'grantType'   : 'client_credentials',
        'clientId'    : client_id,
        'clientSecret': client_secret
    })
    with requests.post(url, headers=headers, data=data) as req:
        response = req.json()

    access_token = response['access_token']
    return access_token


token = ConnectCotoha()   
@app.route('/') 
def index():
    return render_template('index.html')

@app.route("/result", methods=['GET'])
def result():
    sample = []
    for i in range(0,3):
        name = request.args['name']
        wakati = MeCab.Tagger("-Owakati")
        sample.append(wakati.parse(name).split())
    return render_template('test.html',sample = sample)
if __name__ == "__main__":
    app.run(debug=True)