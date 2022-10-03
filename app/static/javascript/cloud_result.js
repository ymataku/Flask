const svg = document.getElementsByTagName('svg')[0]
const panel = document.getElementById('panel')
const test = document.getElementById('test')
svg_text = svg.getElementsByTagName("text")

for(let i = 0;i < svg_text.length;i++){
    svg_text[i].classList.add("svg")
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
                    panel.children[0].innerText = word
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
    svg_text[i].addEventListener(
        "mouseleave",
        function(){
            panel.style.display = "none";
        }
    )
}

