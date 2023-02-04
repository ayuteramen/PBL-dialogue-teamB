# coding: utf-8

import sys
import sentencepiece as spm

def main():
    # センテンスピースのモデル読み込む
    model = spm.SentencePieceProcessor(model_file=sys.argv[2])

    # 分割する
    fname = sys.argv[1]
    fout = open(fname.replace(".txt", ".tok.txt"), "w")
    fin = open(fname, "r")
    for line in fin:
        # try:
        #     tag, speech, response = line.strip().split("\t")
        try:
            speech = line
        except:
            continue
        speech = " ".join(model.encode(speech, out_type=str))
        # response = " ".join(model.encode(response, out_type=str))
        # fout.write(tag + "\t" + speech + "\t" + response + "\n")
        fout.write(speech + "\n")
    fin.close()
    fout.close()


if __name__ == '__main__':
    main()
