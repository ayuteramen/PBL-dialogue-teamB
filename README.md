# PBL-dialogue-teamB 

## 最初に
対話B班では、個性を付与した雑談対話システムを作ることを目的としている。  
ここで言う個性とは年代と性別という属性であり、以降で作成するタグによって個性を制御しようとしている。  
データとしてはTwitterのツイートデータである。  

※所々対話A班と共同で行っている場面があるため、こちらにコードがない場面がある。  
※ここに載せているコードは実際に自分の使っていたものを分かりやすくするために変更しているので、うまくいかない場合がある可能性がある。  



## 前準備
https://github.com/hirokiyamauch/PBL_dialog  
↑この手順の 「1.環境作成」まで行った状態で以下の手順を行う。



## データ収集
ここでは次のファイルを使用している。  
・① collect_data.py  
・② Twitter_API (1).ipynb  

①ではタグなしでとっており、②は年代・性別のタグをつけて収集をしている。  
これらのデータは後の事前訓練、再訓練でそれぞれ使用する。  

"api_key", "api_secret_key", "access_token", "access_token_secret"はTwitterAPIを取得することで分かる。  
TwitterAPIの取得の方法は「Pythonでつくる対話システム」という本の3.4章に記載がされてあった。  
ネットで調べても出てくると思われる。  
※2023/02/09以降TwitterAPIが有料化される模様  

それぞれ、以下の通りに実行する。
'''
python collect_data.py
python Twitter_API.py
'''



## 前処理<タグなしデータ＞
ここでは次のファイルを使用している。  
・① apply-spm.py  
・② pre_data_not_delate_10count.model  
・③ pre_data_not_delate_10count.txt  
・④ bash before_split.sh

<ここで作成するファイル>  
・pre_data_not_deleate_10count.src.train.tok.txt  
・pre_data_not_deleate_10count.tgt.train.tok.txt  
・pre_data_not_deleate_10count.src.valid.tok.txt  
・pre_data_not_deleate_10count.tgt.valid.tok.txt  

"pre_data_not_delate_10count.txt"は「データ収集」の①のファイルを使用して対話A班と共同で集め、A班に前処理を行ってもらったタグなしデータ2144910件のデータである。  
その時の前処理のファイルはA班の方を見に行ってもらいたい。  

単語分割はSentencePieceを用いている。  
SentencePieceは与えられた学習データ（テキスト）から教師なし学習で文字列に分割するためのモデルを生成する。  
①のファイルと②のモデルは対話A班からもらったものなので、②の作成方法はA班のものを見てもらいたい。  

ファイルは以下の通りにして生成する。
'''
bash before_split.sh
'''



## 前処理<タグありデータ＞
前処理として、絵文字・顔文字の除去、文・単語分割を行っている。  

絵文字・顔文字の除去は次のファイルを使用している。  
・tweet_preprocess.py

以下のように絵文字・顔文字除去したいファイル名を指定して実行することで絵文字・顔文字を除去したファイルが生成される。

'''
python3 tweet_preprocess.py [ファイル名]
'''

生成されるファイル名は指定したファイル名の".txt"を"_removed.txt"に置き換えたものになる。

ここでは次のファイルを使用している。  
・① apply-spm.py  
・② pre_data_not_delate_10count.model  
・③ after_text.txt  
・④ after_split.sh

<ここで作成するファイル>
・after.src.train.tok.txt  
・after.tgt.train.tok.txt  
・after.src.valid.tok.txt  
・after.tgt.valid.tok.txt  
・after.src.test.tok.txt  
・after.tgt.test.tok.txt  

"after_text.txt"は「データ収集」の①のファイルを使用して収集し、前処理を行ったタグありデータ156102件のデータである。  
単語分割は「前処理<タグなしデータ＞」と同様にSentencePieceを用いている。  

ファイルは以下の通りにして生成する。  
'''
bash after_split.sh
'''


## 訓練
ここでは次のファイルを使用している。  
・① before_transformer.yaml  
・② after_transformer.yaml  

事前訓練は以下のように行っている。  
ここではタグなしデータ2000000件使用している。
'''
onmt_build_vocab -config "before_transformer.yaml" -n_sample 2000000  
onmt_train -config "before_transformer.yaml"
'''

再訓練は以下のように行っている。  
ここではタグありデータ150000件使用している。  
今回は事前訓練を350000ステップ時のモデルから再開して再訓練している。  
'''
onmt_build_vocab -config "after_transformer.yaml" -n_sample 150000 -skip_empty_level silent -overwrite  
onmt_train -config "after_transformer.yaml" -skip_empty_level silent -update_vocab -reset_optim states -train_from "before_transformer_step_350000.pt"  
'''


## 応答生成
ここでは次のファイルを使用している。  
・① apply-spm.py  
・② pre_data_not_delate_10count.model  
・③ before_test_src.txt  

①では応答生成を行うため、前処理時同様入力文を単語分割している。
"before_test_src.txt"は去年の先輩が使用していた100件のタグなしの発話データである。

'''
python apply-spm.py before_test_src.txt pre_data_not_delate_10count.model　# tokenizeして"before_text_src.tok.txt"作成
'''

今回は事前訓練時の500000ステップ時のモデルの評価を行っている。  
-src ではtokenizeしたテストデータを入力している。  
-output は翻訳結果を出力するファイル名である。  
'''
onmt_translate -model "before_transformer_step_500000.pt" -src "before_test_src.tok.txt" -output "pred.txt"  -verbose  
'''


## 評価
ここでは次のファイルを使用している。  
・① detok-spm.py  
・② bleu.py  
・③ before_test_tgt.txt  
・④ after.tgt.test.tok.txt  

<ここで作成するファイル>  
・after.tgt.test.tok.detok.txt

①のファイル対話A班からもらったものである。   
①ではファイルをdetokenizeしている。ここで"〇〇.detok.txt"というファイルが生成される。  
②ではBLEUの評価値を出している。このとき、正解データ　出力データの順で入力しており、それぞれ単語分けされていない綺麗な文のテキストファイルである。  
"before_test_tgt.txt"は去年の先輩が使用していた100件各8パターンのタグなしの応答データである。 

評価は以下のように行っている。  
<事前訓練時の評価>  
'''
python detok-spm.py "pred.txt"　# detokenizeして"pred.detok.txt"作成  
python bleu.py before_test_tgt.txt pred.detok.txt　# 事前訓練時の評価  
'''

<再訓練時の評価>  
'''
python detok-spm.py "after.tgt.test.tok.txt"　# detokenizeして"after.tgt.test.tok.detok.txt"作成  
python detok-spm.py "pred.txt"　# detokenizeして"pred.detok.txt"作成  
python bleu.py after.tgt.test.tok.detok.txt pred.detok.txt　# 再訓練時の評価  
'''


## Alexaと接続・対話
Alexaとの接続方法は以下のページに記載してある。  
https://github.com/nagaratokuma/PBL_Alexa_.git  

なお、上のページから次の2ファイルを変更している。  
・①alexa_bot.py  
・②generative_system.py  

また、ここでも以下のモデルを使用している。  
・③pre_data_not_delate_10count.model  

ここでは、470000ステップ時のモデルを使用して接続を行っている。  

実行は以下のように変更して行う。
'''
alexa_bot.py -model after_transformer_step_10000.pt -replace_unk -src None  
'''

なお、-modelで指定しているが、結局モデルは②の中で指定をしているので、ここでモデルを指定しても意味がない。  
しかし、ここで-modelを指定しないorないモデルをしていするとおそらくエラーが出ると思われる。

Alexaとの接続ページで「4.接続テスト」の「4.上部のテストタブに移動し、「○○(設定した呼び出し名) を起動」と入力する。」を実行した後のタグの付け方については以下の通りである。

・タグを[年代]にセット  
・タグを[性別]にセット  
・タグを[年代]の[性別]にセット  
・タグをリセット  

[年代] : 10代 / 20代 / 40代  
[性別] : 男性 / 女性  

ここでの年代はそれぞれ以下を指定している。  
10代 : 10代  
20代 : 20～30代  
40代 : 40～60代  


