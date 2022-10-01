const svg = document.getElementsByTagName('svg')[0]
const panel = document.getElementById('panel')
const test = document.getElementById('test')
svg_text = svg.getElementsByTagName("text")

// console.log(typeof(JSON.parse(test.innerText)))

// console.log(svg.getElementsByTagName("text")[0].textContent)
for(let i = 0;i < svg_text.length;i++){
    svg_text[i].classList.add("svg")
    svg_text[i].addEventListener(
        "click",
        function(e){
            word = svg_text[i].textContent
            panel.style.display = "block"
            // console.log(panel.firstChild)
            // console.log(panel.children)
            
            // panel.getElementById('count').innerText = 10
        
            $.ajax({
                // 読み込みの設定
                type: "GET",
                url: "/static/file/data.json", // ファイルパス（相対パス）
                dataType: "json", // ファイル形式
                async: false // 非同期通信フラグ
            }).then(
                function (json) {
                    // 読み込み成功時の処理
                    console.log("読み込みに成功しました");
                    // console.log(json)
                    // console.log(json[word])
                    panel.children[0].innerText = word
                    panel.children[1].innerText = json[word]
                    panel.style.left =  e.clientX;
                    panel.style.top = e.clientY;
                    // json.forEach(function (data) {
                    //     console.log(data)
                    // });
                },
                function () {
                    // 読み込み失敗時の処理
                    console.log("読み込みに失敗しました");
                }
            );
        }
    )
    svg_text[i].addEventListener(
        "mouseleave",
        function(){
            panel.style.display = "none";
        }
    )
}

