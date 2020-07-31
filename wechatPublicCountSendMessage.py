import requests
import json
from globalVar import log


class SendMessage(object):
    """发送信息到微信"""
    appid = "wx852da3a5f145aa40"
    appsecret = "d501c592a2fed6b5daf4334322a55e5e"
    access_token = ""

    def get_access_token(self):
        urlAccessToken = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + \
            SendMessage.appid + "&secret=" + SendMessage.appsecret
        res = requests.get(urlAccessToken)
        SendMessage.access_token = res.json()["access_token"]

    def send_message(self, user_id, template_id, name, price, time):
        """把模板信息发送到指定用户

        Args:
            user_id:用户id，关注该公众号的用户所对应的用户id
            template_id:模板id
            name:股票名称
            price:价格

        """
        urlSendMessage = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + \
            SendMessage.access_token
        param = {
            "touser": user_id,
            "template_id": template_id,
            "topcolor": "#FF0000",
            "data": {
                "name": {
                        "value": name,
                        "color": "#ff0000"
                },
                "price": {
                    "value": price,
                    "color": "#ff0000"
                },
                "time": {
                    "value": time,
                    "color": "#ff0000"
                }
            }

        }
        requests.post(url=urlSendMessage, data=json.dumps(param)).text
        log.logger.info("向用户：{} 发送消息：{}，股票：{}，现价：{}，时间：{}".format(
            user_id, template_id, name, price, time))
