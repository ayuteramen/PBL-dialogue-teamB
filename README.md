# ファイルの説明

## tweet_preprocess.py

収集したツイートから絵文字、一部の顔文字、URL、htmlの特殊文字を除去する。

`tweet_preprocess.py tweet_pairs.txt`のようにツイートペアのtxtファイルを渡して実行すると前処理したtweet_pairs_removed.txtのようなファイルを作成する。

## tweet_pairs_search.py

性別と年代の両方のタグを持ったツイートペアのみのtxtファイルを作成する、

`tweet_pairs_search.py tweet_pairs_removed.txt`のようにツイートペアのtxtファイルを渡して実行すると2つタグを持ったツイートペアのみのtxtファイルを作成する。
