const svg = document.getElementsByTagName('svg')[0]
const panel = document.getElementById('panel')
svg_text = svg.getElementsByTagName("text")

for(let i = 0;i < svg_text.length;i++){
    svg_text[i].classList.add("svg")
    //svgタグ内のtextタグ全てにイベントを仕込む------------------------------------
    svg_text[i].addEventListener(
        "click",
        function(e){
            word = svg_text[i].textContent
            panel.style.display = "block"
            //axiosでバクエンドよりデータを取得------------------------------------
            const option = {responseType: "blob"}
            axios.get('/static/file/data.json',option).then(res => {
                //返ってきたデータをjsonに変換
                res.data.text().then(str => {
                    console.log("読み込みに成功しました");
                    let json = JSON.parse(str)
                    panel.children[0].innerText =  word
                    panel.children[1].innerText = json[word]
                    panel.style.left =  e.clientX;
                    panel.style.top = e.clientY;
                })
            //--------------------------------------------------------------------
               
            }).catch(e => {
                console.log(e)
            })
        }
    )
    //----------------------------------------------------------------------------
}

