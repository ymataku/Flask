from flask import Markup
from wordcloud import WordCloud
def create_wordcloud_svg(word):
    font_path_gothic = './font/ipag.ttf'
    wordcloud = WordCloud(background_color="white",width=1200,height=600,min_font_size=15,font_path=font_path_gothic)
    wordcloud.generate(word)
    cloud = wordcloud.to_svg()
    tag = Markup(cloud)
    return tag