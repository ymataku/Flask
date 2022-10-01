from flask import Flask, render_template,request
import json
import requests
from function.janome import janome_kaiseki
from function.janome import test
from function.wordcloud import create_wordcloud_svg
import json

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
    if not res:
        res = data
    word_list = janome_kaiseki(res)
    word = list_to_string(word_list)
    tag_svg = create_wordcloud_svg(word)
    a = test(word)
    with open("static/file/data.json","w",encoding='utf-8') as f:
        json.dump(a, f, indent=2, ensure_ascii=False)
       
    return render_template('cloud_result.html',tag = tag_svg,test = a,ensure_ascii=False)

if __name__ == "__main__":
    app.run(debug=True)