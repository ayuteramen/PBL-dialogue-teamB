from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request
import echo_system
import generative_system
# Flaskを起動
app = Flask(__name__)
ask = Ask(app, '/')

tag_gender = ''
tag_age = ''

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
    global tag_gender
    tag_gender = gender
    if reset == 'リセット':
        tag_age = ''
        tag_gender = ''
    
##デバッグ用
    print("tag_age = ", tag_age)
    print("tag_gender = ", tag_gender)
    print("reset = ", reset)

# questionでセットしたタグを知らせる
    if tag_age != 'None': response = "タグを'" + str(tag_gender) + str(tag_age) + "'にセットしました。"         # タグが年代だけあるとき
    elif tag_gender != 'None': response = "タグを'" + tag_gender + "'にセットしました。"                        # タグが性別だけあるとき
    else: response = "タグを'" + tag_gender + "', '" + tag_age + "'にセットしました。"                          # タグが両方あるとき
    if reset != 'リセット': return question(response)                                                          # タグをセットしたとき
    else: return question("タグをリセットしました。")                                                           # タグをリセットしたとき    

if __name__ == '__main__':
#   port8080でflaskのサーバを起動
    app.run(port=8080)
