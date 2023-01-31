# 評価（BLEU):最大値で計算した場合
import nltk

def bleu(fname_ref, fname_pred):    
    # 正解文
    f_refs = open(fname_ref, "r")
    refs = [line.rstrip('\n').split("\t") for line in f_refs]
    f_refs.close()
    # 出力文
    f_preds = open(fname_pred, "r")
    preds = [line.strip() for line in f_preds]
    f_preds.close()
    # BLEU
    score_list = []
    for i in range(100):
        max_score = 0
        for j in range(8):
            score = nltk.translate.bleu_score.sentence_bleu(refs[i][j], preds[i], weights = [1])
            if score > max_score:
                max_score = score
        score_list.append(max_score*100)
    avg_score = sum(score_list) / len(score_list)

    return avg_score

"""
ref_file = ".txt" # 正解文
pred_file = ".txt" # 入力文
bleu(ref_file, pred_file)
"""
