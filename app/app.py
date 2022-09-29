from flask import Flask, render_template,request
import json
import requests
from function.janome import janome_kaiseki
from function.wordcloud import create_wordcloud_svg

app = Flask(__name__,static_folder='./static')

def list_to_string(word_list):
    word = ""
    for i in word_list:
        word = word +" "+ i
    return word

@app.route('/',methods=['GET'])
def cloud_get():
    return render_template('cloud.html')

@app.route("/", methods=['POST'])
def cloud_post():
    res =  request.form['text']
    f = request.files.get('file')
    data = f.getvalue().decode("utf-8")
    word_list = janome_kaiseki(data)
    word = list_to_string(word_list)
    tag_svg = create_wordcloud_svg(word)
    if res == "":
        res = data
    return render_template('cloud_result.html',tag = tag_svg)

if __name__ == "__main__":
    app.run(debug=True)