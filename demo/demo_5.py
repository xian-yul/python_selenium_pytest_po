import pymysql  # 导入下载的pymysql包

db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='rootroot',
                     database='demo',
                     charset='utf8')
# 用connec方法连接数据库 host:本机地址 port:端口号 user:用户名 passwd:密码
# database:要操作的数据库 charset:字符集类型


cur = db.cursor()  # 生产游标对象（操作数据库执行sql语句获取结果的对象）
try:
    # 插入操作
    sql = "insert into demo_object values (1,'lw');"
    cur.execute(sql)  # 用ececute方法执行sql语句
    db.commit()  # 提交到数据库执行
except Exception as e:  # 抛出异常(以免程序执行sql语句时报错)
    print(e)
    db.rollback()
# 关闭游标和数据库
cur.close()
db.close()
