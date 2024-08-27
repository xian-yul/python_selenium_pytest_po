import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='rootroot',
                     database='test_demo')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 关闭数据库连接
db.close()
