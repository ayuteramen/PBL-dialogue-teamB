# ①で"pre_data_not_delate_10count.txt"をtokenizeして"pre_data_not_delate_10count.tok.txt"を生成する。
python apply-spm.py pre_data_not_delate_10count.txt pre_data_not_delate_10count.model

# srcとtgtにファイルを分ける
cut -f1 pre_data_not_delate_10count.tok.txt | tr "\t" " " > pre_data_not_delate_10count.src.tok.txt
cut -f2 pre_data_not_delate_10count.tok.txt > pre_data_not_delate_10count.tgt.tok.txt

# train(2000000件)を作成する。
head -2000000 pre_data_not_delate_10count.src.tok.txt > pre_data_not_delate_10count.src.train.tok.txt
head -2000000 pre_data_not_delate_10count.tgt.tok.txt > pre_data_not_delate_10count.tgt.train.tok.txt

# valid(2000件)を作成する。
tail -2000 pre_data_not_delate_10count.src.tok.txt > pre_data_not_delate_10count.src.valid.tok.txt
tail -2000 pre_data_not_delate_10count.tgt.tok.txt > pre_data_not_delate_10count.src.valid.tok.txt