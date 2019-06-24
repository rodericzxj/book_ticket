from splinter.browser import Browser
from time import sleep

 

class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, username, passwd, order, passengers, dtime, starts, ends):
        self.username = username
        self.passwd = passwd
        self.order = order     # 车次，0代表所有车次
        self.passengers = passengers      # 乘客名
        self.starts = starts     # 起始地和终点
        self.ends = ends
        self.dtime = dtime    # 日期
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver_name = 'chrome'
        self.executable_path = 'D:\软件安装处\python\Scripts\chromedriver.exe'
 
    # 登录功能实现
    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name', self.username)
        # sleep(1)
        self.driver.fill('userDTO.password', self.passwd)
        # sleep(1)
        print('输入验证码并点击提交按钮...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break
 

 
    def check_ticket(self):
        print('开始购票...')
        self.driver.cookies.add({"_jc_save_fromStation": self.starts})    # 加载查询信息
        self.driver.cookies.add({"_jc_save_toStation": self.ends})
        self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
        self.driver.reload()
        count = 0
        if self.order != 0:
            while self.driver.url == self.ticket_url:
                self.driver.find_by_text('查询').click()
                count += 1
                print('第%d次点击查询...' % count)
                try:
                    self.driver.find_by_text('预订')[self.order - 1].click()
                    sleep(1.5)
                except Exception as e:
                    print(e)
                    print('预订失败...')
                    continue
        else:
            while self.driver.url == self.ticket_url:
                self.driver.find_by_text('查询').click()
                count += 1
                print('第%d次点击查询...' % count)
                try:
                    for i in self.driver.find_by_text('预订'):
                        i.click()
                        sleep(1.5)
                except Exception as e:
                    print(e)
                    print('预订失败...')
                    continue
        print('开始预订...')
        sleep(1)
        print('开始选择用户...')
        for p in self.passengers:
            self.driver.find_by_text(p).last.click()
            sleep(0.5)
            if p[-1] == ')':
                self.driver.find_by_id('dialog_xsertcj_ok').click()
        type = self.driver.find_by_id('seatType_1')
        type.find_by_tag('option')
        sleep(0.5)
        while True:
            if type.find_by_value('M'):           # 修改对应座次的 value 值，M 表示一等座
                type.find_by_value('M').click()   # 修改对应座次的 value 值，M 表示一等座
                break                             # 二等座的 value 值是大写的 O
            self.driver.visit(self.ticket_url)
            self.check_ticket()
 
 
    # 买票功能实现
    def start_buy(self):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        # 窗口最大化
        self.driver.driver.maximize_window()
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            self.check_ticket()
            print('成功选座')
            sleep(0.5)
            print('提交订单')
            self.driver.find_by_id('submitOrder_id').click()
            sleep(1)
            print('确认选座')
            sleep(1)
            self.driver.find_by_id('qr_submit_id').click()
            print('预订成功')
            sleep(5)
            self.sendMail(mail_title, mail_content)
        except Exception as e:
            print(e)
 
 
if __name__ == '__main__':
    username = 'xxxxxxxx'    # 12306用户名
    password = 'xxxxxxx'    # 12306密码
    order = 3  # 车次选择，0代表所有车次，1表示第一行的车次，2表示第二行的车次，以此类推
    # 乘客名，比如 passengers = ['XXX', 'XXX']
    # 学生票需注明，注明方式为：passengers = ['XXX(学生)', 'XXX']
    passengers = ['张晓杰']
    # 日期，格式为：'2019-01-28'
    dtime = '2019-01-31'
    # 出发地(需填写cookie值)
    starts = '%u4E0A%u6D77%2CAOH'
    # 目的地(需填写cookie值)，在调试模式下点击查询按钮，查看cookie
    ends = '%u5E7F%u5DDE%2CIZQ'
    Buy_Tickets(username, password, order, passengers, dtime, starts, ends).start_buy()