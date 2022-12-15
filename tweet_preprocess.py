import re
import sys

# ファイルを開く
f = open(sys.argv[1], 'r', encoding='utf-8')
f2 = open(sys.argv[1].replace(".txt", "_removed.txt"), 'w', encoding='utf-8')
# ファイルの内容を読み取る
text = f.read()

# 絵文字を除去する　除去したくない文字を指定する。
text = re.sub(r'[^\w\s？！、。‼️…・()（）「」!?.,/～｢｣＼^｡／･＾‥@]', '', text)

#　宛名を除去する
pattern = r"@\S+"
text = re.sub(pattern, "", text)

# 変更された文字列をファイルに書き込む
f2.write(text)

# ファイルを閉じる
f.close()
f2.close()

#除去された文字をtxtファイルに書き込んで確認するために使った
"""
f3 = open('removed_word.txt', 'w', encoding='utf-8')
removed = re.findall(r'[^\w\s？！、。‼️…・()（）「」!?.,/～｢｣＼^｡／･＾‥]', text)
for word in removed:
    f3.write(word)
f3.close()
"""


