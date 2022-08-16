from flask import Flask, render_template,request
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
# token = ""
import json
import requests
from greeting import Hello 
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
   # print(access_token)
def kaiseki(access_token,param):
     sentence = param
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

token = ConnectCotoha()   
@app.route('/') 
def index():
    
    title = token
    return render_template('index.html',title = title)

@app.route("/result", methods=['GET'])
def result():
    # sample = np.array(['Apple computer of the apple mark', 'linux computer', 'windows computer'])
    # vec_count = CountVectorizer()
    # vec_count.fit(sample)
    # X = vec_count.transform(sample)
    # vector = X.toarray()
    sample = []
    name = request.args['name']
    # result = ConnectCotoha(name)
    print("check1")
    result = kaiseki(token,name)
    print("check2")
    print(result)
    for i in result['result']:
        for j in i['tokens']:
            sample.append(j['form'])

    return render_template('test.html',sample = sample)

if __name__ == "__main__":
    app.run(debug=True)