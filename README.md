# PBL-dialogue-teamB 

## データ収集
データ収集では次の二つのファイルを使用している。  
① collect_data.py  
② Twitter_API (1).ipynb  
①ではタグなしでとっており、②は年齢・性別のタグをつけて収集をしている。  
これらのデータは後の事前訓練、再訓練でそれぞれ使用する。  



## 前処理
前処理として、絵文字・顔文字の除去、文分割を行っている。  


文分割はSentencePieceを用いている。SentencePieceは与えられた学習データ（テキスト）から教師なし学習で文字列に分割するためのモデルを生成する。  
モデルは以下のものを使用している。このモデルは対話A班からもらったもので、作成方法はA班のものを見てもらいたい。  
pre_data_not_delate_10count.model  



## 訓練


## 評価


## Alexaと接続・対話
Alexaとの接続方法は以下のページに記載してある。  
https://github.com/nagaratokuma/PBL_Alexa_.git
なお、上のページから次の2ファイルを変更している。  

