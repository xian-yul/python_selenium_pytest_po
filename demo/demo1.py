# # # areas = ["'黑龙江'", "'辽宁'", "'吉林'", "'河北'", "'河南'", "'湖北'", "'湖南'", "'山东'", "'山西'", "'陕西'", "'安徽'",
# # #          "'浙江'",
# # #          "'江苏'",
# # #          "'福建'", "'广东'", "'海南'", "'四川'",
# # #          "'云南'", "'贵州'", "'青海'", "'甘肃'", "'江西'", "'台湾'", "'上海'", "'天津'", "'重庆'", "'内蒙古'", "'宁夏'",
# # #          "'新疆'",
# # #          "'西藏'",
# # #          "'广西'"]
# # # for item in areas:
# # #     print(item)
# #
# # place_order = {'org_name': '丹山', 'shop_num': '1', 'pickup_type': 4, 'sign_type': 2, 'billing_type': 0,
# #                'deposit': 5, 'multiple_type': 0, 'multiple_order': 3, 'hide_type': 1}
# #
# # place = {}
# #
# # name = input('输入要进行搜索企业名称:')
# # shop_num = input('输入要进行购买的商品数量:')
# # mistake_num = 1
# # while True:
# #     pickup_type = int(input('请输入下单类型(1自提款到发货  2配送款到发货 3配送定金 4自提定金) :'))
# #     if pickup_type == 1 or pickup_type == 2 or pickup_type == 3 or pickup_type == 4:
# #         mistake_num = 1
# #         break
# #     else:
# #         print('输入的内容错误 请输入正确的内容, 错误次数 ' + str(mistake_num))
# #         mistake_num += 1
# # sign_type = input('输入协议签署类型(1个人签署 2企业签署 ):')
# # billing_type = input('输入开票类型 (1开票 0不开票):')
# # deposit = float(input('输入定金比例:'))
# # multiple_type = int(input('输入订单是否多发多提 (0多发 1一次性):'))
# # multiple_order = int(input('输入订单多发或多提的单数:'))
# # hide_type = input('输入是否要隐藏收货地址(1隐藏  0不隐藏):')
# # place['name'] = name
# # place['shop_num'] = shop_num
# # place['pickup_type'] = pickup_type
# # place['sign_type'] = sign_type
# # place['billing_type'] = billing_type
# # place['deposit'] = deposit
# # place['multiple_type'] = multiple_type
# # place['multiple_order'] = multiple_order
# # place['hide_type'] = hide_type
# # print(place)
# str1 = '（剩余集采：988吨）'
# str1 = str1[6:-2]
# num = 10
# if num < int(str1):
#     print('2')
# print(str1)
import time

str1 = '2023-03-07 09:40'
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))