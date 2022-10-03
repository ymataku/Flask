from flask import Flask, render_template,request
import json
import requests
from function.janome import janome_kaiseki
from function.janome import calc_frequency_word
from function.wordcloud import create_wordcloud_svg
import json

app = Flask(__name__,static_folder='./static')

# janomeからの返り値を文字列に直す
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
    hinsi = request.form['hinsi']
    f = request.files.get('file')
    data = f.getvalue().decode("utf-8")
    if not res:
        res = data
    if not res:
        return render_template('./cloud.html',err = "解析対象が含まれていません。")
    # wordcloudをsvgで作成----------------------------------------
    # janome.pyファイルで形態素解析をしたものをリストで出力
    word_list = janome_kaiseki(res,hinsi)
    word = list_to_string(word_list)
    if not word:
        return render_template('./cloud.html',err = "指定した品詞が含まれてません。")
    tag_svg = create_wordcloud_svg(word)
    # -----------------------------------------------------------


    # jsonファイルに単語の出現頻度を出力----------------------------
    word_frequency_dic = calc_frequency_word(word)
    with open("static/file/data.json","w",encoding='utf-8') as f:
        json.dump(word_frequency_dic, f, indent=2, ensure_ascii=False)
    # ------------------------------------------------------------

    return render_template('cloud_result.html',tag = tag_svg,test = word_frequency_dic)

if __name__ == "__main__":
    app.run(debug=True)