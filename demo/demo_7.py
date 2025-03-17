import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_object.JsbOperaProductAudit import JsbOperaProductAudit
from utils import util
from utils.log import Log

log = Log()

page_url = {'goods_list': 'http://192.168.101.24:8070/product-manage/products-list/raw',
            'goods_add_page': 'http://192.168.101.24:8070/product-manage/raw-provide-form'
    , 'opera_audit': 'http://192.168.101.24:8050/operateManage/goods-list/row-material-examine-table',
            'user_order_list': 'http://v3.www.jinsubao.test/user-center/my-order-list',
            'seller_order_list': 'http://192.168.101.24:8070/order-manage/order-list'}
delivery_method = 1  # 1自提 2 配送
pay_method = 1  # 1款到 2 定金
raw_method = 1  # 1现货 2 基差

chrome_options = Options()  # 创建一个事项
chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:9234')  # ip地址为第一步中在浏览器中输入的地址
driver = webdriver.Chrome(options=chrome_options)
num = 0
for num in range(0, 20):
    # driver.find_elements(By.XPATH, "// h3[@class='purchase-order-e']")[0].click()
    util.ec_all_elements(driver, "// h3[@class='purchase-order-e']", 0)
    time.sleep(1)
    if raw_method == 1:
        # driver.find_elements(By.XPATH, "// button[@class='w-1/2 cursor-pointer']")[1].click()
        util.ec_all_elements(driver, "// button[@class='w-1/2 cursor-pointer']", 1)
    else:
        # driver.find_elements(By.XPATH, "// button[@class='w-1/2 cursor-pointer']")[0].click()
        util.ec_all_elements(driver, "// button[@class='w-1/2 cursor-pointer']", 0)
    time.sleep(1)
    if delivery_method == 1:
        # driver.find_element(By.XPATH, "// button[@id='logisticsMode-one']").click()
        util.ec_element(driver, "// button[@id='logisticsMode-one']")
    else:
        # driver.find_element(By.XPATH, "// button[@id='logisticsMode-two']").click()
        util.ec_element(driver, "// button[@id='logisticsMode-two']")
    time.sleep(1)
    if pay_method == 2 and raw_method == 1:
        # driver.find_element(By.XPATH, "// button[@id='goodsDelivery-two']").click()
        util.ec_element(driver, "// button[@id='goodsDelivery-two']")
    util.input_clear_text(driver.find_element(By.XPATH,
                                              "// input[@class='input-number-input size-full outline-none pl-2.5 pr-2.25  svelte-6hukl4']"),
                          1)
    driver.find_element(By.XPATH, "// div[@class='text-secondly-default']").click()
    time.sleep(1)
    driver.find_element(By.XPATH,
                        "// button[@class='ring-offset-background focus-visible:ring-ring inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-secondly-400 px-4 py-2 w-47.5 h-10.5 rounded-1 text-white bg-secondly-default']").click()
    if raw_method == 2:
        time.sleep(1)
        driver.find_element(By.XPATH,
                            "// button[@class='ring-offset-background focus-visible:ring-ring inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 text-primary-foreground hover:bg-secondly-400 h-9 rounded-md px-3 bg-secondly-default']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "// button[@class='ring-offset-background focus-visible:ring-ring inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 text-primary-foreground hover:bg-secondly-400 ml-5 px-3.75 py-1.5 h-8 bg-secondly-default']").click()
    time.sleep(3)
    driver.get(page_url['seller_order_list'])
    time.sleep(5)
    util.ec_all_elements(driver, "// span[@class='w-button-group-item']", 0)
    time.sleep(3)
    print('点击了订单详情')
    if raw_method == 1 and pay_method == 2:
        util.input_clear_text(driver.find_element(By.XPATH, "// input[@id='proportion']"), 10)
    if raw_method == 2:
        # driver.find_element(By.XPATH, "// button[@class='ant-btn ant-btn-primary']").click()
        util.ec_element(driver, "// button[@class='ant-btn ant-btn-primary']")
        time.sleep(1)
        # driver.find_element(By.XPATH, "// button[@class='ant-btn ant-btn-primary']")[1].click()
        util.ec_all_elements(driver, "// button[@class='ant-btn ant-btn-primary']", 1)

    else:
        # driver.find_elements(By.XPATH, "// button[@class='ant-btn ant-btn-primary']")[1].click()
        util.ec_all_elements(driver, "// button[@class='ant-btn ant-btn-primary']", 1)
    util.ec_all_elements(driver, "// button[@class='ant-btn ant-btn-primary']", -1)
    print('点击了生成合同')
    time.sleep(100)
    util.signing_contract(driver, time)
    time.sleep(2)
    driver.get(page_url['user_order_list'])
    time.sleep(3)
    util.ec_element(driver, "// button[@class='ant-btn ant-btn-primary ant-btn-sm']")
    time.sleep(1)
    driver.find_elements(By.XPATH, "// button[@class='ant-btn ant-btn-primary']")[1].click()
    time.sleep(20)
    util.signing_contract(driver, time)
    num += 1
