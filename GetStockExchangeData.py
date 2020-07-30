import requests
import json
import time


token_time = int(str(time.time_ns())[0:10])  # 保存公众号token获取时间，以便每隔一段时间进行更新


class StockInfo(object):
    """股票信息对象"""
    dictStock = {}  # 存放股票代码及查询链接
    stockData = []  # 存放获取到的股票信息

    def __init__(self, monitoredStock):
        """构造函数，初始化要监控的股票极其链接.
        Args:
            monitoredStock:要监控的股票代码，格式为：股票代码[,股票代码]，字符串类型
        """
        self.monitoredStock = monitoredStock

        for stockNum in str.split(monitoredStock, ","):
            StockInfo.dictStock.setdefault(
                stockNum, "http://yunhq.sse.com.cn:32041//v1/sh1/snap/" + stockNum)

    def __get_data(self, url):
        """获取股票数据.

        Args:
            url:股票的链接
        """
        response = requests.get(url)
        jsonData = response.json()
        StockInfo.stockData.append((jsonData["snap"][0], jsonData["code"], jsonData["snap"][5], jsonData["snap"][7], jsonData["snap"]
                                    [6], jsonData["snap"][1], jsonData["snap"][2], jsonData["snap"][3], jsonData["snap"][4], jsonData["time"]))

    def get_all_stock_info(self):
        """获取所有的股票信息."""
        for url in StockInfo.dictStock.values():
            StockInfo.__get_data(self, url)
        StockInfo.stockData.sort(
            key=lambda stock: stock[3], reverse=True)  # 以涨幅进行排序

    def display_stock_info(self):
        """显示所有的股票信息"""
        for data in StockInfo.stockData:
            print("{}({}) 现价：{:<7.2f} 涨幅：{:7s} 涨跌：{:<6.2f} 昨收：{:<7.2f} 开盘：{:<7.2f} 最高：{:<7.2f} 最低：{:<7.2f} 交易时间：{}".format(
                data[0], data[1], data[2], str(data[3])+"%", data[4], data[5], data[6], data[7], data[8], data[9]), sep="")


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


stockInfo = StockInfo(
    "600685,600072,600009,601318,600276,601788,600030,600519,600999")
sendMessage = SendMessage()

stockInfo.get_all_stock_info()
sendMessage.get_access_token()

# stockInfo.display_stock_info()


def check_current_price(alert_price):
    """检查所有股票的现价是否达到要提醒的价位.

    Args:
        alert_price:是一个dict,key=股票号(str),value=提醒价位(str[,str])

    """
    for data in stockInfo.stockData:
        if data[1] in alert_price.keys():
            if str(data[2]) in alert_price.get(data[1]).split(","):
                global token_time
                if int(str(time.time_ns())[0:10]) - token_time > 6600:
                    sendMessage.get_access_token()
                    token_time = int(str(time.time_ns())[0:10])
                sendMessage.send_message(
                    "oE8HjwmATpXWJIPqzMVhbKBYTEBc", "nG2Z4dL21oKuAYSVqHrUwp8_QbGoB4lct6AYw1ld7HA", data[0], str(data[2]), data[9])


alert_price = {"600685": "40,41,39", "600072": "14,15",
               "600009": "67", "601788": "23", "600999": "21,21.20,21.50"}


def loopFunc(func, param, second):
    looping = True
    while looping:
        if time.localtime().tm_hour > 15:
            looping = False
            break
        func(param)
        time.sleep(second)


loopFunc(check_current_price, alert_price, 3)


# 以下是测试代码

# check_current_price(alert_price)

# response = requests.get(
#     "http://yunhq.sse.com.cn:32041//v1/sh1/snap/600999")
# jsonData = response.json()
# print(jsonData["snap"][0], "(", jsonData["code"], ")", " 现价：", jsonData["snap"][5], " 涨幅：", jsonData["snap"][6], " 涨跌：", jsonData["snap"][7], " 昨收：",
#       jsonData["snap"][1], " 开盘：", jsonData["snap"][2], " 最高：", jsonData["snap"][3], " 最低：", jsonData["snap"][4], " 交易时间：", jsonData["time"], sep="")
