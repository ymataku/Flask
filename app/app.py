from flask import Flask, render_template,request
import numpy as np
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import json
import requests
from greeting import Hello 
import MeCab
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

token = ""

app = Flask(__name__,static_folder='./static')
#firebaseの接続設定
cred = credentials.Certificate('./db-test-63ae0-firebase-adminsdk-id4g0-7f9f362c75.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://db-test-63ae0-default-rtdb.firebaseio.com/',
    'databaseAuthVariableOverride': {
        'uid': '111279736261474156340'
    }
})

users_ref = db.reference('/users')

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

def parse(res):
    m = MeCab.Tagger()
    word=""
    # sample = []
    node = m.parseToNode(res)
    while node:
        hinshi = node.feature.split(",")[0]
        # sample.append(node.feature.split(","))
        if hinshi in ["名詞","動詞","形容詞"]:
            origin = node.feature.split(",")[6]
            word = word + " " + origin
        node = node.next
    return word


token = ConnectCotoha()   
@app.route('/') 
def index():
    return render_template('index.html')

@app.route("/result", methods=['GET'])
def result():
    sample = []
    sample2 = []
    sample3 = []
    index = 0
    name = request.args['name']
    mecab = MeCab.Tagger()
    sample.append(mecab.parse(name).split("\n"))
    for i in sample[0]:
        sample2.append(i.split('\t'))
    
    while sample2[index][0] != "EOS":
        sample3.append({"word":sample2[index][0],"pos":sample2[index][4]})
        index = index + 1
    return render_template('test.html',sample = sample,sample2 = sample2,sample3 = sample3)

@app.route('/cloud',methods=['GET'])
def make():
    return render_template('cloud.html')

@app.route("/cloud", methods=['POST'])
def cloud():
    res =  request.form['text']
    f = request.files.get('file')
    data = f.getvalue().decode("utf-8")
    if res == "":
        res = data
    font_path_gothic = './font/ipag.ttf'
    wordcloud = WordCloud(width=600,height=400,min_font_size=15,font_path=font_path_gothic)
    try:
        wordcloud.generate(parse(res))
        wordcloud.to_file("./static/img/wordcloud.png")
    except:
        return render_template('error.html',error=parse(res))
    return render_template('cloud_result.html')

@app.route('/db',methods=['GET'])
def form():
    title = "ng"
    return render_template('db.html',title = title)

@app.route('/db',methods=['POST'])
def post():
    name = request.form['name']
    age = request.form['age']
    # databaseにデータを追加する
    users_ref.child(name).set({
        'age': age,
        })
    title = "OK"
    return render_template('db.html',title = title)

@app.route('/other')
def other():
    return 'Other World\n'
  

if __name__ == "__main__":
    app.run(debug=True)