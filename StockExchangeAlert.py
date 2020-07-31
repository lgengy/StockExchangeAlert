import time
from globalVar import log
from stockInfo import StockInfo
from wechatPublicCountSendMessage import SendMessage


token_time = int(str(time.time_ns())[0:10])  # 保存公众号token获取时间，以便每隔一段时间进行更新

stockInfo = StockInfo(
    "600685,600072,600009,601318,600276,601788,600030,600519,600999")
sendMessage = SendMessage()
sendMessage.get_access_token()
alert_price = {"600685": ([37.63, 37.11, 37.15], 0), "600072": ([13.72, 13.76, 13.82], 0),
               "600009": ([67.80, 67.76, 67.65], 0), "601788": ([23.11, 23.05, 23.15], 0), "600999": ([21.45, 28.20, 25.32], 0)}
for key, value in alert_price.items():
    log.logger.info("代码：" + key + "  告警价位：" + str(value[0]))


def check_current_price(alert_price):
    """检查所有股票的现价是否达到要提醒的价位.

    Args:
        alert_price:是一个dict,key=股票号(str),value=提醒价位(str[,str])

    """
    for data in stockInfo.stockData:
        if data[1] in alert_price.keys():  # 判断是否为要告警的股票
            x = alert_price.get(data[1])[0]
            if data[2] in x:  # 判断是否为要告警的价位
                if alert_price.get(data[1])[1] < 3:  # 判断告警次数是否超过3次
                    global token_time
                    if int(str(time.time_ns())[0:10]) - token_time > 6600:
                        sendMessage.get_access_token()
                        token_time = int(str(time.time_ns())[0:10])
                    sendMessage.send_message(
                        "oE8HjwmATpXWJIPqzMVhbKBYTEBc", "nG2Z4dL21oKuAYSVqHrUwp8_QbGoB4lct6AYw1ld7HA", data[0], str(data[2]), data[9])
                    log.logger.info("股票：{} 第{}次告警".format(
                        data[1], alert_price.get(data[1])[1] + 1))
                    alert_price[data[1]] = (alert_price.get(
                        data[1])[0], alert_price.get(data[1])[1]+1)


def loopFunc(func, param, second):
    looping = True
    while looping:
        if time.localtime().tm_hour > 15:
            looping = False
            break
        stockInfo.get_all_stock_info()
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
