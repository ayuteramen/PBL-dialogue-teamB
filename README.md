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
再訓練は以下のようにして行っている。今回は事前訓練を350000ステップ時のモデルから再開して再訓練している。
onmt_build_vocab -config "transformer.yaml" -n_sample 150000 -skip_empty_level silent -overwrite　　
onmt_train -config "transformer.yaml" -skip_empty_level silent -update_vocab -reset_optim states -train_from "new_transformer_step_350000.pt"


## 評価
評価は以下のファイルを使っている。
bleu.py  

## Alexaと接続・対話
Alexaとの接続方法は以下のページに記載してある。  
https://github.com/nagaratokuma/PBL_Alexa_.git
なお、上のページから次の2ファイルを変更している。  

