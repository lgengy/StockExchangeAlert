from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import checkboxlist_dialog, yes_no_dialog, input_dialog, message_dialog
from prompt_toolkit.styles import Style


class SystemUI(object):
    """交互界面"""

    def __init__(self):
        self.__se_info = None  # 存放交易所信息
        self.__se_selected = False  # 交易所是否已选中标志
        self.__alert_price = {}  # 要告警的交易所、股票及价位

    def interactive_start(self):
        """选择交易所"""
        self.__se_info = checkboxlist_dialog(
            title="请选择股票交易所",
            text="使用上下键和Tab键进行切换，Enter键选中",
            ok_text="确认",
            cancel_text="取消",
            values=[
                ("上交所", "上交所"),
                ("上交所ETF", "上交所ETF"),
                ("深交所", "深交所"),
            ],
            style=Style.from_dict(
                {
                    "dialog": "bg:#cdbbb3",
                    "button": "bg:#bf99a4",
                    "checkbox": "#e8612c",
                    "dialog.body": "bg:#a9cfd0",
                    "dialog shadow": "bg:#c98982",
                    "frame.label": "#fcaca3",
                    "dialog.body label": "#fd8bb6",
                }
            ),
        ).run()
        if self.__se_info is not None:  # 如果是None则说明用户选择了取消，退出系统
            self.__se_is_selected()  # 此时__se_info有两种情况，分别为[]和非空

    def __se_is_selected(self):
        """判断交易所是否已选择"""
        if self.__se_info:  # 非空
            self.__se_selected = yes_no_dialog(
                title="确认",
                text="你选中了: %s" % ",".join(self.__se_info),
                yes_text="确认",
                no_text="返回"
            ).run()

            if not self.__se_selected:  # 选择了返回，则回到交易所选择界面
                self.interactive_start()
            else:
                self.__alert_stock_selecting()

        else:  # 空
            message_dialog(
                title='提示',
                text='尚未选中交易所信息！').run()
            self.interactive_start()

    def __alert_stock_selecting(self):
        """输入需要告警的股票代码及价位(600685:价1,价n)，多个股票代码以;间隔"""
        for se in self.__se_info:
            alert = ''
            while alert.strip() == '':
                alert = input_dialog(
                    title="请输入需要告警的股票代码及价位,格式：600685:价1[,价n][;600685:价1[,价n]]",
                    text=se,
                    ok_text="确认",
                    cancel_text="返回",
                    style=Style.from_dict(
                        {
                            "dialog.body": "bg:#a9cfd0",
                            "dialog.body label": "#fd8bb6"
                        })
                ).run()
            else:
                self.__alert_price[se] = alert

    def get_monitored_stock(self):
        dict_stock_info = {}
        for key, value in self.__alert_price.items():
            stock_info = {}
            for stock in value.split(';'):
                get_stock_id = stock.split(':')
                dict_price = {}
                for price in get_stock_id[1].split(','):
                    dict_price.update({float(price): 0})
                stock_info.update({get_stock_id[0]: dict_price})
            dict_stock_info.update({key: stock_info})
        return dict_stock_info


interactive_prompt = SystemUI()
interactive_prompt.interactive_start()
interactive_prompt.get_monitored_stock_number()
