import re
import sys

# ファイルを開く
f2 = open(sys.argv[1].replace(".txt", "_searched.txt"), 'w', encoding='utf-8')
# txtファイルを開く
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    # 各行を取得する
    lines = f.readlines()

# 各行をループ処理する
for line in lines:
    # 各行から、<>で囲われたタグを抽出する
    tags = re.findall(r'<.*?>', line)
    # 抽出したタグの数をカウントする
    count = len(tags)
    # タグの数が2の場合は、その行をファイルに書き込む
    if count == 2:
        f2.write(line)
        print(line)

# ファイルを閉じる
f.close()
f2.close()
