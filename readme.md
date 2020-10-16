爬取上海证券交易所指定代码的股票信息

1、该程序使用的公众号是微信提供的测试号，网址https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
2、SendMessage类输入微信公众号的appid和appsecret用以获取access_token
3、SendMessage类的send_message方法第一二个参数需要传入关注公众号用的ueseid和公众号发送消息模板的templateid
4、日志存放目录：E:\practice\SSECrawier\log\
