import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn)

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

#ここの＠はデコレータ。　appのroute関数を、callback関数を引数にわたして　実行してる。
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    # notesのCarouselColumnの各値は、変更してもらって結構です。
    notes = [CarouselColumn(thumbnail_image_url="https://vps14-d.kuku.lu/files/20200726-1232_3ea73866bb9a2087de50eb757324b646.jpg",
                            title="【ReleaseNote】MindMap",
                            text="冴えた決断力を手にしたいアナタへ。",
                            actions=[{"type": "uri","label": "詳しくはこちら","linkuri": "https://sketchboard.me/JCfPOpNMvTkL#/"}]),

             CarouselColumn(thumbnail_image_url="https://vps16-d.kuku.lu/files/20200726-1234_11ba60e794c05be607cfe8ed9a388a33.png",
                            title="【自己紹介】",
                            text="エンジニアとしての技術的記事をゆる～くまとめています。",
                            actions=[
                                {"type": "message", "label": "詳しくはこちら", "text": "https://qiita.com/maruda"}]),

             CarouselColumn(thumbnail_image_url="https://vps16-d.kuku.lu/files/20200726-1236_81ff3a2f63cb3501b7dfa08e1fe4a2da.png",
                            title="【ReleaseNote】公式アカウントをリリース！",
                            text="各種サービスに繋げるQRコードを生成しました。",
                            actions=[
                                {"type": "uri", "label": "友達追加はこちら", "linkuri": "https://renttle.jp/notes/kota/5"}])]

    messages = TemplateSendMessage(
        alt_text='template',
        template=CarouselTemplate(columns=notes),
    )

    line_bot_api.reply_message(event.reply_token, messages=messages)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

