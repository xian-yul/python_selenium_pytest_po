"""
@author: luhx
需安装库: pip install sqlalchemy==2.0.29
@file: data_base_manage.py
@desc: sqlalchemy的封装类，实现pd的read,connection的execute
"""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, TimeoutError
from typing import Callable
import pandas as pd
import logging
import socket
import time


class DatabaseManager:
    """
    DatabaseManager is responsible for handling database connections and operations.
    from urllib import parse
    pwd_encoded = parse.quote_plus(password)
    db_param should be a string in the form:
    'mysql+pymysql://user:pwd_encoded@host:port/database'
    where pwd_encoded is the URL encoded password.
    """

    def __init__(self, conn_info: str, max_retries: int = 0):
        self.db_param = db_param
        self.engine = create_engine(db_param, pool_pre_ping=True)  # Enable pool pre-ping
        self.connection = self._connect()
        self.max_retries = max_retries
        self.delay_second = 1.0  # 默认出错了重视前应等待一定时间c

    def _connect(self):
        try:
            return self.engine.connect()
        except OperationalError as e:
            logging.error(f"Failed to connect to the database: {e}")
            return None

    def _reconnect(self):
        if self.connection:
            self.connection.close()
        self.connection = self._connect()

    def query(self, sql: str):
        return self._retry_operation(self._query, sql)

    def _query(self, sql: str):
        if not self.connection:
            self._reconnect()
        return pd.read_sql_query(sql, self.connection)

    def execute(self, sql: str):
        return self._retry_operation(self._execute, sql)

    def _execute(self, sql: str):
        if not self.connection:
            self._reconnect()
        rel = self.connection.execute(text(sql))
        self.connection.commit()
        return rel

    def _retry_operation(self, operation: Callable, sql: str):
        retries = 0
        while self.max_retries == 0 or retries < self.max_retries:
            try:
                return operation(sql)
            except (OperationalError, TimeoutError, socket.error) as e:
                logging.error(f"An operational error occurred: {e}. Attempting to reconnect.")
                time.sleep(self.delay_second)
                self._reconnect()
                retries += 1
            except Exception as e:
                logging.error(f"An error occurred during SQL execution: {e}")
                break
        logging.error(f"Operation failed after {self.max_retries} retries.")
        return None

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()


# 示例用法
if __name__ == "__main__":
    # 第一种用法,需要显示调用close
    db_param = 'mysql+pymysql://user:pwd_encoded@host:port/database'
    db_manager = DatabaseManager(db_param)
    sql = "SELECT * FROM your_table WHERE condition;"
    result = db_manager.query(sql)
    if result is not None:
        print(result)  # 输出查询结果
    else:
        print("Query failed.")
    db_manager.close()
    # 第二种用法，无需显示调用close
    db_param = 'mysql+pymysql://user:pwd_encoded@host:port/database'
    with DatabaseManager(db_param) as db_manager:
        result = db_manager.query("SELECT * FROM some_table")
        print(result)
