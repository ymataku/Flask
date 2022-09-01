from flask import Flask, render_template,request
import numpy as np
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import json
import requests
from greeting import Hello 
import MeCab
token = ""

app = Flask(__name__,static_folder='./static')
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
    test = []
    node = m.parseToNode(res)
    while node:
        hinshi = node.feature.split(",")[0]
        try:
            if hinshi in ["名詞","形容詞"]:
                origin = node.feature.split(",")[8]
                test.append(node.feature.split(","))
                word = word + " " + origin
        except:
            test.append(node.feature.split(","))
        node = node.next
    return word,test


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
    wordcloud = WordCloud(background_color="white", width=600,height=400,min_font_size=15,font_path=font_path_gothic)
    word,test = parse(res)
    try:
        wordcloud.generate(word)
        wordcloud.to_file("./static/img/wordcloud.png")
    except:
        return render_template('error.html',error=parse(res))
    return render_template('cloud_result.html')

if __name__ == "__main__":
    app.run(debug=True)