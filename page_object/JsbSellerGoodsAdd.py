from selenium.webdriver.common.keys import Keys

from common.readelement import Element
from page.webpage import WebPage
from utils.log import Log
from utils.times import sleep

goods = Element('JsbSellerGoodsAdd')
log = Log()

seller_url = {'24': 'http://192.168.101.24:8070/user/login', '20': 'https://slrdm.jinsubao.cn/',
              '24_登录后': 'http://192.168.101.24:8070/dashboard', '20_登录后': 'https://slrdm.jinsubao.cn/dashboard',
              '供需列表': 'http://192.168.101.24:8070/product-manage/purchase-index/purchase-list',
              '24_raw_list': 'http://192.168.101.24:8070/product-manage/products-list/raw',
              '20_raw_list': 'https://slrdm.jinsubao.cn/product-manage/products-list/raw',
              '24_raw_add': 'http://192.168.101.24:8070/product-manage/raw-provide-form',
              '20_raw_add': 'https://slrdm.jinsubao.cn/product-manage/raw-provide-form',
              '24_product_list': 'http://192.168.101.24:8070/product-manage/products-list/product',
              '20_product_list': 'https://slrdm.jinsubao.cn/product-manage/products-list/product',
              '原料': 0, '制成品': 1,
              '船货': 2,
              '24_coupon_list': 'http://192.168.101.24:8070/marketing-manage/coupon-list',
              '24_coupon_add': 'http://192.168.101.24:8070/marketing-manage/creat-coupon/&1',
              '20_coupon_list': 'https://slrdm.jinsubao.cn/marketing-manage/coupon-list',
              '20_coupon_add': 'https://slrdm.jinsubao.cn/marketing-manage/creat-coupon/&1',
              '24_order_list': 'http://192.168.101.24:8070/order-manage/order-list',
              '20_order_list': 'https://slrdm.jinsubao.cn/order-manage/order-list'}


class JsbSellerGoodsAdd(WebPage):

    def seller_add_goods_type(self, addGoods):
        sleep(0.5)
        self.find_elements(goods['添加商品'])[0].click()
        sleep(0.2)
        self.find_elements(goods['添加商品类型'])[seller_url[addGoods]].click()
        sleep(0.2)
        log.info('所选添加商品类型为 :' + addGoods)

    def goods_put_on_shelves(self):
        sleep(0.2)
        self.find_elements(goods['列表_上架按钮'])[0].click()
        sleep(0.2)
        self.find_elements(goods['列表_确定'])[2].click()
        try:
            state = self.find_elements(goods['列表状态'])[0].text
            flag = '审核中' in state
            if flag:
                log.info('上架审核成功')
                sleep(0.5)
        except AssertionError:
            log.info('上架审核出错')
            self.fial_info()

    def goods_upload(self, img_path, video_path):
        sleep(0.2)
        self.find_elements(goods['上传'])[1].send_keys(img_path)
        sleep(0.5)
        self.find_elements(goods['上传'])[0].send_keys(video_path)

    def goods_add_submit(self, serve, goodsNumber, img_path, video_path, type, number, circulation):
        sleep(0.5)
        self.find_elements(goods['提交按钮'])[0].click()
        sleep(0.5)
        try:
            if serve == '24':
                assert self.return_current_url() == seller_url['24_raw_list']
            else:
                assert self.return_current_url() == seller_url['20_raw_list']
            log.info('原料新增成功____新增牌号为: ' + str(goodsNumber))
            self.goods_put_on_shelves()
            goodsNumber += 1
            return goodsNumber
        except AssertionError:
            log.info('原料添加出错__牌号' + str(goodsNumber) + ' 重复__下次添加牌号为 :  ' + str(goodsNumber + 1))
            goodsNumber += 1
            sleep(0.5)
            self.goods_grade(goodsNumber, type, number, circulation)
            sleep(0.2)
            self.goods_upload(img_path, video_path)
            sleep(0.2)
            self.goods_add_submit(serve, goodsNumber, img_path, video_path, type, number, circulation)
            sleep(0.2)

    def goods_deliver(self, included, deliveryPrice, deliveryDays):
        if included == 1:  # 价格含税判断
            self.find_elements(goods['原料_单选按钮'])[1].click()
        self.is_click(goods['配送范围'])
        sleep(0.2)
        self.is_click(goods['配送范围_全部'])
        sleep(0.1)
        self.is_click(goods['配送范围_确定'])
        self.find_elements(goods['原料_复选框按钮'])[2].click()  # 配送定金
        self.find_elements(goods['原料_复选框按钮'])[3].click()  # 配送款到
        self.input_clear_text(goods['配送价格'], deliveryPrice)
        self.input_clear_text(goods['发货时间'], deliveryDays)

    def goods_mention(self, included, selfMentionPrice, selfMentionDays):
        sleep(0.2)
        self.find_elements(goods['原料_复选框按钮'])[1].click()
        self.find_elements(goods['原料_单选按钮'])[2].click()
        if included == 1:  # 价格含税判断
            self.find_elements(goods['原料_单选按钮'])[3].click()
        self.find_elements(goods['原料_复选框按钮'])[4].click()  # 自提款到
        self.find_elements(goods['原料_复选框按钮'])[5].click()  # 自提定金
        self.input_clear_text(goods['自提价格'], selfMentionPrice)
        self.input_clear_text(goods['提货时间'], selfMentionDays)

    def seller_raw_add(self, serve, sellerPhone, addGoods, goodsDeliver, included, stockNum, minPurchase, deliveryPrice,
                       deliveryDays
                       , selfMentionPrice, selfMentionDays, profiles, detail, goodsNumber, video_path, img_path, limit,
                       add_type, number, circulation):
        addNum = 1
        self.seller_phone_login(serve, sellerPhone)
        self.is_click(goods['产品管理'])
        self.is_click(goods['产品列表'])
        while addNum <= limit:
            log.info('--------------------------------------------------------------------------')
            log.info('当前新增牌号为 : ' + str(goodsNumber))
            self.seller_add_goods_type(addGoods)
            self.goods_grade(goodsNumber, add_type, number, circulation)
            self.input_clear_text(goods['原料库存'], stockNum)
            self.input_clear_text(goods['原料最低采购'], minPurchase)
            if goodsDeliver == 1:  # 单配送
                self.goods_deliver(included, deliveryPrice, deliveryDays)
                log.info('当前原料添加方式为 单配送')
            elif goodsDeliver == 2:  # 单自提
                self.goods_mention(included, selfMentionPrice, selfMentionDays)
                log.info('当前原料添加方式为 单自提')
            elif goodsDeliver == 3:  # 配送 + 自提
                self.goods_deliver(included, deliveryPrice, deliveryDays)
                self.goods_mention(included, selfMentionPrice, selfMentionDays)
                log.info('当前原料添加方式为 配送 + 自提')
            self.goods_upload(img_path, video_path)
            log.info('进行原料上传图片 / 视频')
            self.input_clear_text(goods['内容简要'], profiles)
            iframe = self.find_element(goods['iframe框架'])
            self.driver.switch_to.frame(iframe)
            sleep(0.5)
            self.input_text(goods['商品详情'], detail)
            self.driver.switch_to.default_content()
            self.goods_add_submit(serve, goodsNumber, img_path, video_path, add_type, number, circulation)
            goodsNumber += 1
            log.info('当前新增次数 : ' + str(addNum) + '  预计新增次数  : ' + str(limit))
            addNum += 1

    def seller_product_add(self, serve, sellerPhone, addGoods, title, subtitle, keywords, code, producingArea, needSign,
                           material, brand, address, img_path, video_path, sku_name, sku_price, sku_min_purchase,
                           sku_stock, sku_weight, profiles, detail, limit):
        addNum = 0
        self.seller_phone_login(serve, sellerPhone)
        self.is_click(goods['产品管理'])
        self.is_click(goods['产品列表'])
        while addNum <= limit:
            self.seller_add_goods_type(addGoods)
            self.input_clear_text(goods['制成品_标题'], title + "_____" + str(addNum))
            self.input_clear_text(goods['制成品_简略标题'], subtitle)
            self.input_clear_text(goods['制成品_产品编号'], code)
            self.input_clear_text(goods['制成品_产地'], producingArea)
            self.input_clear_text(goods['制成品_材质'], material)
            self.input_clear_text(goods['制成品_品牌'], brand)
            if needSign == 1:
                self.is_click(goods['制成品_合同'])
            self.find_elements(goods['制成品_商品分类'])[0].click()
            self.find_elements(goods['制成品_分类选择'])[0].click()
            sleep(0.2)
            self.find_elements(goods['制成品_关键字'])[0].send_keys(keywords)
            sleep(0.2)
            self.find_elements(goods['制成品_关键字'])[0].send_keys(Keys.ENTER)
            self.find_elements(goods['制成品_制塑工艺'])[1].click()
            sleep(0.2)
            self.find_elements(goods['制成品_制塑工艺选择'])[0].click()
            self.find_elements(goods['制成品_制塑工艺选择'])[1].click()
            self.find_elements(goods['制成品_物流模板'])[4].click()
            sleep(0.2)
            self.find_elements(goods['制成品_物流选择'])[-1].click()
            sleep(0.3)
            self.is_click(goods['制成品_发货地点'])
            sleep(0.2)
            self.click_area()
            self.input_clear_text(goods['制成品_详细地址'], address)
            self.find_elements(goods['上传'])[0].send_keys(img_path)
            self.input_clear_text(goods['制成品_规格名称'], sku_name)
            self.input_clear_text(goods['制成品_规格单价'], sku_price)
            self.input_clear_text(goods['制成品_最低采购'], sku_min_purchase)
            self.input_clear_text(goods['制成品_库存'], sku_stock)
            self.input_clear_text(goods['制成品_重量'], sku_weight)
            self.find_elements(goods['上传'])[2].send_keys(img_path)
            sleep(0.5)
            self.find_elements(goods['上传'])[1].send_keys(video_path)
            self.input_clear_text(goods['内容简要'], profiles)
            iframe = self.find_element(goods['iframe框架'])
            self.driver.switch_to.frame(iframe)
            sleep(0.5)
            self.input_text(goods['商品详情'], detail)
            self.driver.switch_to.default_content()
            self.find_elements(goods['提交按钮'])[0].click()
            sleep(0.5)
            try:
                if serve == '24':
                    assert self.return_current_url() == seller_url['24_product_list']
                else:
                    assert self.return_current_url() == seller_url['20_product_list']
                log.info('制成品新增成功')
                sleep()
                self.goods_put_on_shelves()
                log.info('当前新增次数 : ' + str(addNum) + '  预计新增次数  : ' + str(limit))
                addNum += 1
            except AssertionError:
                self.fial_info()

    def ceseee(self, serve, seller_phone, limit):
        log.info(212131313)
        self.seller_phone_login(serve, seller_phone)
        self.is_click(goods['产品管理'])
        self.is_click(goods['产品列表'])
        num = 0
        num1 = 1
        sleep(0.2)
        while num < limit:
            self.find_elements(goods['列表_上架按钮'])[num].click()
            sleep(0.2)
            self.find_elements(goods['列表_确定'])[2].click()
            state = self.find_elements(goods['列表状态'])[0].text
            flag = '审核中' in state
            if flag:
                log.info('上架审核成功')
                sleep(0.5)
            if num == 9:
                self.find_elements(goods['卖家原料页码'])[num1].click()
                num = 0
                num1 += 1
            else:
                num += 1
            log.info(num)
