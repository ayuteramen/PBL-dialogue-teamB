cut -f1 after_text.txt > after_text_tag.txt　# タグだけのデータ
cut -f2 after_text.txt > after_text_src.txt　# 発話だけのデータ
cut -f3 after_text.txt > after_text_tgt.txt　# 応答だけのデータ

# そのままtokenizeするとタグが分割されてしまうため、タグを分けてからtokenizeを行う。
python apply-spm.py after_text_src.txt pre_data_not_delate_10count.model　# tokenizeして"after_text_src.tok.txt"作成 python apply-spm.py after_text_tgt.txt pre_data_not_delate_10count.model　# tokenizeして"after_text_tgt.tok.txt"作成

paste -d " " after_text_src.tok.txt after_text_tag.txt > after.src.tok.txt 　# 発話＋タグのデータ

head -150000 after.src.tok.txt > after.src.train.tok.txt　# train(150000件)作成
head -150000 after_text_tgt.tok.txt > after.tgt.train.tok.txt　# train(150000件)作成
tail -3000 after.src.tok.txt | head -1500 > after.src.valid.tok.txt　# valid(1500件)作成
tail -3000 after_text_tgt.tok.txt | head -1500 > after.tgt.valid.tok.txt　# valid(1500件)作成
tail -300 after.src.tok.txt > after.src.test.tok.txt　 # test(300件)作成
tail -300 after_text_tgt.tok.txt > after.tgt.test.tok.txt　# test(300件)作成