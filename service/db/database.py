#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/8/10 上午8:18
@file: mysqlExec
@author: nothing4any
Description:
"""

import aiomysql

from core.config import settings
from utils.logger import database_log


class DataBase(object):

    def __init__(self):
        self.logger = database_log

    async def init(self):
        ip = settings.DBIP
        port = int(settings.DBPORT)
        user = settings.DBUSER
        pwd = settings.DBPWD
        database = settings.DBDATABASE
        maxsize = int(settings.DBMAXSIZE)
        # 数据库连接参数
        db_config = {
            'host': ip,
            'port': port,
            'user': user,  # 使用提供的用户名
            'password': pwd,  # 替换为实际密码
            'db': database,  # 替换为实际使用的数据库名
            'minsize': 1,  # 最小连接数
            'maxsize': maxsize,  # 最大连接数
        }
        try:
            self.pool = await aiomysql.create_pool(**db_config)
            # self.LOG_KEY["normal"].info('------数据库连接池 创建完成------')
        except Exception as e:
            self.logger.error('数据库连接异常 {}'.format(e))
            return 1

    async def execute(self, sql: str, para=None):
        result = 0
        if para is None:
            para = ()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    self.logger.info(f"执行的sql {sql}")
                    if len(para) != 0:
                        self.logger.info(f"执行的参数 {para}")
                    await cursor.execute(sql, para)
                    await conn.commit()
                    result = await cursor.fetchall()
                except Exception as e:
                    self.logger.error(f"数据执行异常 {e}")
                    await conn.rollback()
                finally:
                    # conn.close()
                    pass
        return result

    async def executemany(self, sql: str, para=None):
        result = 0
        if para is None:
            para = ()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    self.logger.info(f"执行的sql {sql}")
                    if len(para) != 0:
                        self.logger.info(f"执行的参数 {para}")
                    await cursor.executemany(sql, para)
                    await conn.commit()
                    result = await cursor.fetchall()
                except Exception as e:
                    self.logger.error(f"数据执行异常 {e}")
                    await conn.rollback()
                finally:
                    # conn.close()
                    pass
        return result
