from onmt.translate.translator import build_translator
import onmt.opts as opts
from onmt.utils.parse import ArgumentParser
import MeCab
import sentencepiece as spm
import subprocess


class GenerativeSystem:
    def __init__(self):
        # おまじない
        parser = ArgumentParser()
        opts.config_opts(parser)
        opts.translate_opts(parser)
        self.opt = parser.parse_args()
        ArgumentParser.validate_translate_opts(self.opt)
        self.translator = build_translator(self.opt, report_score=True)

        # センテンスピースに変える
        ###
        # # 単語分割用にMeCabを使用
        # self.mecab = MeCab.Tagger("-Owakati")
        # self.mecab.parse("")
        self.tokenizer = spm.SentencePieceProcessor()
        self.tokenizer.Load("pre_data_not_delate_10count.model")
        ### 

    def initial_message(self, input):
        return {'utt': 'こんにちは。対話を始めましょう。', 'end': False}

    def reply(self, input):
        # 単語を分割
        ###
        print('分割前')
        print(input["utt"])
        # src = [self.mecab.parse(input["utt"])[0:-2]]
        if "\t" in input["utt"]:
            text, tag = input["utt"].split("\t")
            src = ' '.join(self.tokenizer.EncodeAsPieces(text)) + " " + tag
        else:
            text = input["utt"]
            tag = ""
            src = ' '.join(self.tokenizer.EncodeAsPieces(text))
        # タグを付加
        # src = input["Tag"] + src
        # アンダーバー除去
        # src = [src.replace("▁", "")]
        
        ###
        print('分割後')
        print(src)
        ###
        # print(input["Tag"])

        # OpenNMTで応答を生成
        # scores, predictions = self.translator.translate_batch(
        #     src=src,
        #     tgt=None,
        #     src_dir=self.opt.src_dir,
        #     batch_size=self.opt.batch_size,
        #     attn_debug=False
        # )
        fout = open("/home/teramen/honban/tmp-src.txt", "w")
        fout.write(src + "\n")
        fout.close()
        command = list()
        command.append("onmt_translate")
        command.append("-model")
        command.append("after_transformer_step_470000.pt")
        command.append("-src")
        command.append("tmp-src.txt")
        command.append("-output")
        command.append("tmp-pred.txt")
        command.append("-gpu")
        command.append("0")
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        print(result)
        # result = subprocess.run(["ls", "-l"], stdout=subprocess.PIPE, text=True)
        # onmt_translate -model "/home/teramen/honban/model2_350000/transformer_step_410000.pt" -src "/home/teramen/honban/tag_test_src.tok.txt" -output "/home/teramen/honban/pred.txt" -gpu "0" -verbose
        fin = open("/home/teramen/honban/tmp-pred.txt", "r")
        results = [line.strip() for line in fin]
        fin.close()
        # OpenNMTの出力も単語に分割されているので，半角スペースを削除
        ###    
        # utt = predictions[0][0].replace("▁ ", "")
        # utt = self.tokenizer.DecodePieces(predictions[0][0].split())  
        utt = self.tokenizer.DecodePieces(results[0].split())  
        ###
        return {'utt': utt, "end": False}


if __name__ == '__main__':
    system = GenerativeSystem()
    bot = TelegramBot(system)
    bot.run()

    











# from onmt.translate.translator import build_translator
# import onmt.opts as opts
# from onmt.utils.parse import ArgumentParser
# import MeCab
# import sentencepiece as spm



# class GenerativeSystem:
#     def __init__(self):
#         # おまじない
#         parser = ArgumentParser()
#         opts.config_opts(parser)
#         opts.translate_opts(parser)
#         self.opt = parser.parse_args()
#         ArgumentParser.validate_translate_opts(self.opt)
#         self.translator = build_translator(self.opt, report_score=True)

#         # センテンスピースに変える
#         ###
#         # # 単語分割用にMeCabを使用
#         # self.mecab = MeCab.Tagger("-Owakati")
#         # self.mecab.parse("")
#         self.tokenizer = spm.SentencePieceProcessor()
#         self.tokenizer.Load("/home/teramen/honban/pre_data.model") # パスを変更する！
#         ### 

#     def initial_message(self, input):
#         return {'utt': 'こんにちは。対話を始めましょう。', 'end': False}

#     def reply(self, input):
#         # 単語を分割
#         ###
#         # src = [self.mecab.parse(input["utt"])[0:-2]]
#         src = [self.tokenizer.EncodeAsPieces(input["utt"])]
#         ###
#         print(src)
#         # OpenNMTで応答を生成
#         scores, predictions = self.translator.translate(
#             src=src,
#             tgt=None,
#             src_dir=self.opt.src_dir,
#             batch_size=self.opt.batch_size,
#             attn_debug=False
#         )
#         # OpenNMTの出力も単語に分割されているので，半角スペースを削除
#         ###    
#         # utt = predictions[0][0].replace("▁ ", "")
#         utt = self.tokenizer.DecodePieces(predictions[0][0].split())  
#         ###
#         return {'utt': utt, "end": False}


# if __name__ == '__main__':
#     system = GenerativeSystem()
#     bot = TelegramBot(system)
#     bot.run()

    
