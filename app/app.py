from flask import Flask, render_template,request
import numpy as np
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import json
import requests
from greeting import Hello 
import MeCab
from flask import Markup

token = ""

app = Flask(__name__,static_folder='./static')

def parse(res):
    m = MeCab.Tagger()
    word=""
    # sample = []
    node = m.parseToNode(res)
    while node:
        hinshi = node.feature.split(",")[0]
        # sample.append(node.feature.split(","))
        
        if hinshi in ["名詞","動詞","形容詞"]:
            try:
                print("OK")
                origin = node.feature.split(",")[6]
            except:
                print("erro")
            word = word + " " + origin
        node = node.next
    return word

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
    word = parse(res)
    wordcloud.generate(word)
    cloud = wordcloud.to_svg()
    tag = Markup(cloud)
        # wordcloud.to_file("./static/img/wordcloud.png")
    return render_template('cloud_result.html',tag=tag,ts = cloud)


@app.route('/other')
def other():
    return 'Other World\n'
  

if __name__ == "__main__":
    app.run(debug=True)