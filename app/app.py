from flask import Flask, render_template,request
import json
import requests
from function.janome import janome_kaiseki
from function.wordcloud import create_wordcloud

token = ""

app = Flask(__name__,static_folder='./static')

def parse(x):
    word = ""
    for i in x:
        word = word +" "+ i
    return word

@app.route('/') 
def index():
    janome = janome_kaiseki("すもももももももものうち")
    return render_template('index.html',janome = janome)


@app.route('/',methods=['GET'])
def make():
    return render_template('cloud.html')

@app.route("/", methods=['POST'])
def cloud():
    res =  request.form['text']
    f = request.files.get('file')
    data = f.getvalue().decode("utf-8")
    word_list = janome_kaiseki(data)
    word = parse(word_list)
    tag_svg = create_wordcloud(word)
    # test = type(test)
    # if res == "":
    #     res = data
   

    return render_template('cloud_result.html',tag = tag_svg)


@app.route('/other')
def other():
    return 'Other World\n'
  

if __name__ == "__main__":
    app.run(debug=True)