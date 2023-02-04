# PBL-dialogue-teamB 

## データ収集
データ収集では次のファイルを使用している。  
① collect_data.py  
② Twitter_API (1).ipynb  
①ではタグなしでとっており、②は年齢・性別のタグをつけて収集をしている。  
これらのデータは後の事前訓練、再訓練でそれぞれ使用する。  



## 前処理
前処理として、絵文字・顔文字の除去、文分割を行っている。  


文分割はSentencePieceを用いている。SentencePieceは与えられた学習データ（テキスト）から教師なし学習で文字列に分割するためのモデルを生成する。  
モデルは以下のものを使用している。このモデルは対話A班からもらったもので、作成方法はA班のものを見てもらいたい。  
・pre_data_not_delate_10count.model  



## 訓練
訓練は次のファイルを使用している。
・before_transformer.yaml  
・after_transformer.yaml  

事前訓練は以下のように行っている。  
onmt_build_vocab -config "before_transformer.yaml" -n_sample 2000000
onmt_train -config "before_transformer.yaml"

再訓練は以下のようにして行っている。今回は事前訓練を350000ステップ時のモデルから再開して再訓練している。  
onmt_build_vocab -config "after_transformer.yaml" -n_sample 150000 -skip_empty_level silent -overwrite　　
onmt_train -config "after_transformer.yaml" -skip_empty_level silent -update_vocab -reset_optim states -train_from "before_transformer_step_350000.pt"

## 翻訳
翻訳は以下のように行っている。
onmt_translate -model "before_transformer_step_500000.pt" -src "test_data.tok.txt" -output "pred.txt"  -verbose 



## 評価
評価は以下のファイルを使っている。
① detok-spm.py  
② bleu.py  
①では翻訳で出力されたファイルをdetokenizeしている。これは、②で入力するファイルの形を整えるためである。  
②ではBLEUの評価値を出している。このとき、正解データ　出力データの順で入力しており、それぞれ単語分けされていない綺麗な文のテキストファイルである。  
実行は以下のように行っている。  
python detok-spm.py "pred.txt"  
python bleu.py test_ans.txt pred.detok.txt  



## Alexaと接続・対話
Alexaとの接続方法は以下のページに記載してある。  
https://github.com/nagaratokuma/PBL_Alexa_.git
なお、上のページから次の2ファイルを変更している。  
alexa_bot.py  
generative_system.py  
