from flask import Flask, render_template
import numpy as np
import json
import requests
from sklearn.feature_extraction.text import CountVectorizer

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
    # print(access_token)

    sentence = 'すもももももももものうち'
    url = 'https://api.ce-cotoha.com/api/dev/nlp/v1/parse'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': f'Bearer {access_token}'
    }

    data = json.dumps({
        'sentence': sentence
    })
    with requests.post(url, headers=headers, data=data) as req:
        response = req.json()
    # 分かち書き
    # for i in response['result']:
    #     for j in i['tokens']:
    #         print(j['form'])
    return response
        

@app.route('/', methods=['GET', 'POST']) 
def index():
    sample = np.array(['Apple computer of the apple mark', 'linux computer', 'windows computer'])
    vec_count = CountVectorizer()
    vec_count.fit(sample)
    X = vec_count.transform(sample)
    vector = X.toarray()

    test = 'hello world'
    res = ConnectCotoha()
    sample = res['result'][0]['tokens'][0]['form']
    version = vector[0]
    return render_template('index.html',test = test,sample = sample,version = version)

@app.route("/create")
def create():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)