### Morphological_Analysis
<br>
<img src ="https://cloud.githubusercontent.com/assets/17031124/22752754/0eec7c16-ee7d-11e6-86bf-f0bc1bf0e8b6.png" ALT="SAMPLE" title="IMG"><br>
<br>
[Slide](https://speakerdeck.com/xxxhal/webtekisutochu-li "Slide")
<br>

・概要<br>
福澤諭吉の「学問のススメ」を、ジョジョの奇妙な冒険風に呟くBot<br>
学問のススメ全体からランダムに一文を取得し、取得した一文をジョジョっぽい文体にしてつぶやく<br>
※ ジョジョっぽい文体とは<br>
・語尾の母音が伸びる<br>
・語尾に「ッ」「ー」「！」が入る<br>
・独特な名言が多い<br>
・重要な単語が「」でくくられる<br>
<br>
・処理<br>
1. 文章取得 BeautifulSoup4(スクレイピングライブラリ)を使って、 Webサイトから学問のすすめ全文を取得。全文を句点(。)でsplitし、 その中からランダムに一つをrandom.choice()で選ぶ。<br>
<br>
2. 形態素解析 上記で取得した1文を形態素解析(MeCabのChasen形式)にかけ、 単語それぞれの「品詞」と「読み」を取得しリストに保存。
<br><br>
3. ジョジョ文体化 
形態素解析の「読み」から助詞と末尾の単語の最後の文字を取得し、 母音を判別。あらかじめ定数で用意した語尾リストから、 母音に適したものを選び、本文の文字列に付け足す。
文頭と文末にも、あらかじめ定数で用意したジョジョ名言リストから ランダムに取得し文字列に付け足す。<br><br>
4. ツイート 上記までで作られた文字列を毎時55分にツイートする
<br>


--------------- 追記 ---------------<br>
<br>
![screen shot 2017-02-09 at 03 58 40](https://cloud.githubusercontent.com/assets/17031124/22752343/87306892-ee7b-11e6-9914-62f6ed4fafd4.png)
