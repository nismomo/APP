from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定 Channel access token 與 Channel secret
line_bot_api = LineBotApi('kFqnIIAuE6ebbRko8QYMV24ExzxsyKqb1mHs3EAtq1zw0KgyRXowCbtE+ae/xdN6ZtEQCbJDixh7i0WCXYDvz/DHo9SLXpBzBVHbUT33C5rofn1v5bqCwAJiQfUY63MA2CwjSRyRj9NxMf+7Hc1zwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4ccc7b4e377493d6780cd9c1766749c6')

# 設定允許訪問的關鍵字和圖片對應的 URL
image_urls = {
    '熊': ['https://imgbox.com/9nbNYETk', 'https://imgbox.com/v0eOpEce'],
    'Bear': ['https://imgbox.com/9nbNYETk', 'https://imgbox.com/v0eOpEce'],
    'bear': ['https://imgbox.com/9nbNYETk', 'https://imgbox.com/v0eOpEce'],
    '熊(Bear).jpg': 'https://imgbox.com/9nbNYETk',
    '熊(Bear).png': 'https://imgbox.com/v0eOpEce',
    '兔': 'https://imgbox.com/TrTt4LWW',
    'Rabbit': 'https://imgbox.com/TrTt4LWW',
    'rabbit': 'https://imgbox.com/TrTt4LWW',
    '貓': 'https://imgbox.com/U0KbQUDj',
    'Cat': 'https://imgbox.com/U0KbQUDj',
    'cat': 'https://imgbox.com/U0KbQUDj'
}

# 接收 LINE 的訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text in image_urls:
        images = image_urls[text]
        if isinstance(images, list):
            for image_url in images:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=image_url)
                )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=images)
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Sorry, I cannot find the image.")
        )

if __name__ == "__main__":
    app.run()
