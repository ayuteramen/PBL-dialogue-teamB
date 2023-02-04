from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request
import echo_system
import generative_system
# Flaskを起動
app = Flask(__name__)
ask = Ask(app, '/')

tag_gender = None
tag_age = None

# 対話システムを起動
#system = echo_system.EchoSystem()
system = generative_system.GenerativeSystem()
# alexaから送られてきたテキストのうち，最も長いもの（＝ユーザの発話）を抜き出すためのメソッド
def marge_texts(texts):
    text = ''
    for t in texts:
        try:
            if len(t) >= len(text):
                text = t
        except: pass
    
    return text

# 起動した時に呼び出されるインテント
@ask.launch
def launch():
    # 発話はなし，session.sessionIdでセッションIDを取得してinitial_messageを返答
    speech_text = "こんにちは。対話を始めましょう。"
    print(question(speech_text))
    return question(speech_text) #.reprompt(speech_text).simple_card('Helloworlds', speech_text)
    """
    response = system.initial_message({"utt":"","sessionId":session.sessionId})
    print("utt = ", response['utt'])
    welcome_message = render_template("hello")
    return question(response['utt'])
    #return question(response).reprompt(response).simple_card('HelloWorld', response)
    """
# ユーザが話しかけた時に呼び出されるインテント
# mappingはalexaから送られてきたスロット（情報）をどのような変数名で受け取るかを定義している
@ask.intent('HelloIntent', mapping={'any_text_a': 'any_text_a', 'any_text_b': 'any_text_b','any_text_c': 'any_text_c', })
def talk(any_text_a, any_text_b, any_text_c):
#   受け取ったスロットをまとめて，長いものを抜き出す
    texts = [ any_text_a, any_text_b, any_text_c ]
    text = marge_texts(texts)

##   デバッグ用
    print("text = ", text)

#   タグを付ける
    global tag_age, tag_gender
##  デバッグ用
    print("tag_age = ", tag_age)
    print("tag_gender = ", tag_gender)
    tag = ''
    if tag_age is not None:
        if tag_age == '10代':
            tag = '<10代>'
        elif tag_age == '20代':
            tag = '<20～30代>'
        elif tag_age == '40代':
            tag = '<40～60代>'

    if tag_gender is not None: tag = tag + ' <' + str(tag_gender) + '>' 
    # tag = tag.replace(' ', '') #空白を削除
    text = text + "\t" + tag #
##  デバッグ用
    print("text = ", text)

#   ユーザ発話を対話システムの応答生成に与える，セッションIDもsession.sessionIdで取得する

    mes = system.reply({"utt":text,"sessionId":session.sessionId})

#   この発話で終了する時はstatement（この発話でスキルを終了する）で応答
    if mes['end']: return statement(mes['utt'])
#   この発話で終了しない場合はquestion（ユーザの応答を待つ）で応答
    else: return question(mes['utt'])

# タグを設定するときに呼び出されるインテント
@ask.intent('TagIntent', mapping={'gender': 'Gender', 'age': 'Age', 'reset': 'Reset'})
def tag(gender, age, reset):
#   タグをセットする
    global tag_age 
    tag_age = age
    if tag_age is not None:tag_age = tag_age.replace(' ', '')
    global tag_gender
    tag_gender = gender
    if tag_gender is not None:tag_gender = tag_gender.replace(' ', '')
    if reset == 'リセット':
        tag_age = None
        tag_gender = None
    
##デバッグ用
    print("tag_age = ", tag_age)
    print("tag_gender = ", tag_gender)
    print("reset = ", reset)

# questionでセットしたタグを知らせる
    tag_response = ''
    if tag_age is not None: tag_response = str(tag_age)                                               # タグが年代だけあるとき
    if tag_gender is not None: tag_response = tag_response + str(tag_gender)                        # タグが性別だけあるとき
    response = "タグを'" + tag_response + "'にセットしました。"                          # タグが両方あるとき
    if reset != 'リセット': return question(response)                                                          # タグをセットしたとき
    else: return question("タグをリセットしました。")                                                           # タグをリセットしたとき    

if __name__ == '__main__':
#   port8080でflaskのサーバを起動
    app.run(port=8080)
