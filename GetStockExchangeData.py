import time
from log import Log
from stockInfo import StockInfo
from wechatPublicCountSendMessage import SendMessage


token_time = int(str(time.time_ns())[0:10])  # 保存公众号token获取时间，以便每隔一段时间进行更新

stockInfo = StockInfo(
    "600685,600072,600009,601318,600276,601788,600030,600519,600999")
sendMessage = SendMessage()

log = Log("E:\\practice\\SSECrawier", "right", "wrong")
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
               "600009": "68.34", "601788": "23", "600999": "21,21.20,21.50"}


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
