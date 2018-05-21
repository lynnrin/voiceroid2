# -*- coding: utf-8 -*-
import tweepy
import re
import PlayFromCmd
import time

# API用のキー
CUSTOMER_KEY = "YHTrWD3aQDY8VGf71xvsmixKk"
CUSTOMER_SECRET = "I3c6QdwXLK2BfPHTDtl6QSUEZXzmH3gmV3tccenZ2dxCj4cHo2"
ACCESS_TOKEN = "2324056879-YmJo7luSdKt8mfRo1AocdhTqKhPOoGob425nFQG"
ACCESS_TOKEN_SECRET = "BYT7nQ3zmBuLbOrrPGKgr1VTdYvzkL2vfSHJ0jUz7jRIU"

# 1.override StreamListener
# StreamingListenerをオーバーライド
class ReplyStreamListener(tweepy.StreamListener):
    # Statusが届いたら確認する
    def on_status(self, status):
        # 対象に対するリプライ？
        if str(status.in_reply_to_screen_name) == self.api.me().screen_name:
            # リプライ者とその文言を取得する
            name = status.user.name
            text = status.text
            # 文言から「@ユーザ名」を除く
            text = re.sub('@[A-Za-z0-9_]+','',text)
            # 文言からURLを抜く
            text = re.sub('https?://[a-zA-Z0-9./\-=]*','',text)
            # 話す文言を作る
            phrase = "{0}さんからリプライです。\n{1}".format(name,text)
            # 出力
            # print(phrase)
            # # VOICEROID2に指示を出す
            PlayFromCmd.talkVOICEROID().talk(phrase)

    # エラー発生時
    def on_error(self,status_code):
        print('ErrorCode:{0}'.format(status_code))
        return True

    # タイムアウト発生時
    def on_timeout(self):
        print('Timeout Occured...')
        return True

    def getStringFromTwitter(self):
        # OAuthの準備
        auth = tweepy.OAuthHandler(CUSTOMER_KEY,CUSTOMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

        # TwitterAPIハンドル取得
        self.api = tweepy.API(auth)
        replyStream = tweepy.Stream(auth = self.api.auth, listener = self)

        # 3.ストリームの開始
        # statuses/filterのfollowで選別する
        replyStream.filter(follow = [self.api.me().id_str])


ReplyStreamListener().getStringFromTwitter()