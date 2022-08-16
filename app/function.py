
class Cotoha:
    
    # https://api.ce-cotoha.com/contents/reference.html の
    # リファレンスにあるやつ。でも面倒だから書きたくないよね。
     def c(client_id,client_secret,url):
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
    
     def Keitaiso(token,word):

        sentence = word
        url = 'https://api.ce-cotoha.com/api/dev/nlp/v1/parse'
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': f'Bearer {access_token}'
        }

        data = json.dumps({
            'sentence': sentence
        })
        with requests.post(url, headers=headers, data=data) as req:
            response = req.json()
        # 分かち書き
        # for i in response['result']:
        #     for j in i['tokens']:
        #         print(j['form'])
        return response
     