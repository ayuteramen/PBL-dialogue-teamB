# PBL-dialogue-teamB 

## データ収集
データ収集では次のファイルを使用している。  
・① collect_data.py  
・② Twitter_API (1).ipynb  
①ではタグなしでとっており、②は年齢・性別のタグをつけて収集をしている。  
これらのデータは後の事前訓練、再訓練でそれぞれ使用する。  
"api_key", "api_secret_key", "access_token", "access_token_secret" はTwitterAPIを取得することで分かる。  
TwitterAPIの取得の方法は「Pythonでつくる対話システム」という本の3.4章に記載がされてあった。  
ネットで調べても出てくると思われる。  
※TwitterAPIが有料化される模様  



## 前処理
前処理として、絵文字・顔文字の除去、文分割を行っている。  


文分割はSentencePieceを用いている。  
SentencePieceは与えられた学習データ（テキスト）から教師なし学習で文字列に分割するためのモデルを生成する。  モデルは以下のものを使用している。このモデルは対話A班からもらったもので、作成方法はA班のものを見てもらいたい。  
・pre_data_not_delate_10count.model  



## 訓練
訓練は次のファイルを使用している。  　
・before_transformer.yaml  
・after_transformer.yaml  

事前訓練は以下のように行っている。  
ここではタグなしデータ2000000件使用している。
onmt_build_vocab -config "before_transformer.yaml" -n_sample 2000000  
onmt_train -config "before_transformer.yaml"  

再訓練は以下のようにして行っている。  
ここではタグありデータ150000件使用している。  
今回は事前訓練を350000ステップ時のモデルから再開して再訓練している。  
onmt_build_vocab -config "after_transformer.yaml" -n_sample 150000 -skip_empty_level silent -overwrite  
onmt_train -config "after_transformer.yaml" -skip_empty_level silent -update_vocab -reset_optim states -train_from "before_transformer_step_350000.pt"  



## 翻訳
翻訳は以下のように行っている。  
今回は事前訓練時の500000ステップ時のモデルの評価を行っている。  
-src ではtokenizeしたテストデータを入力している。  
-output は翻訳結果を出力するファイル名である。  
onmt_translate -model "before_transformer_step_500000.pt" -src "test_data.tok.txt" -output "pred.txt"  -verbose  



## 評価
評価は以下のファイルを使っている。  
・① detok-spm.py  
・② bleu.py  
①では翻訳で出力されたファイルをdetokenizeしている。これは、②で入力するファイルの形を整えるためである。  
②ではBLEUの評価値を出している。このとき、正解データ　出力データの順で入力しており、それぞれ単語分けされていない綺麗な文のテキストファイルである。  
実行は以下のように行っている。  
python detok-spm.py "pred.txt"  
python bleu.py test_ans.txt pred.detok.txt  



## Alexaと接続・対話
Alexaとの接続方法は以下のページに記載してある。  
https://github.com/nagaratokuma/PBL_Alexa_.git  
なお、上のページから次の2ファイルを変更している。  
・alexa_bot.py  
・generative_system.py  
また、ここでも以下のモデルを使用している。  
・pre_data_not_delate_10count.model  
ここでは、470000ステップ時のモデルを使用して接続を行っている。
