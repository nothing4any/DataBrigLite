#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/12/1 20:28
@author: nothing4any
@file: catchdata
@Project: dataplatform-server
@Software: PyCharm
@Description: 创建 本地数据 缓存,可以切换redis;仅仅用于登陆和接口认证
"""

import cachetools
import redis
from core.config import settings
import sys

from utils.logger import main_log

is_redis = settings.IS_REDIS
"""
本地缓存支持1000人登录
# 添加缓存项
cache["key"] = "value"
# 此时缓存项已过期，尝试获取时将返回默认值
value = cache.get("key", "default_value")
"""
logger = main_log


# 创建一个最大容量为1000,每个元素过期时间为7天秒的缓存

class CatchTool:

    def __init__(self):
        self.cache = None
        if is_redis:
            self.__pool = redis.ConnectionPool(host=settings.REDISIP, port=int(settings.REDISPORT), db=0,
                                               decode_responses=True)
            self.r = None
            try:
                r = redis.Redis(connection_pool=self.__pool, host=settings.REDISIP, port=int(settings.REDISPORT)
                                , db=0, password=settings.REDISPWD)  # 或者用redis.StrictRedis
                r.auth(settings.REDISPWD)
                r.ping()
            except Exception as e:
                logger.error("redis连接失败，请检查redis服务或者配置文件")
                sys.exit(1)

    def get_catch_client(self):
        if is_redis:
            self.cache = self.r
        else:
            self.cache = cachetools.TTLCache(maxsize=1000, ttl=60 * 24 * 7)

    def set_data(self, token, name, key, role, expire=None):
        """
        :param token:
        :param name: username
        :param key: userid
        :param role: 角色
        :param expire:
        :return:
        """
        if is_redis:
            obj = self.cache.get_obt()
            if expire is None:
                expire = 60 * 24 * 7
            obj.set(name=token, value=f'{name}_{key}_{role}', ex=int(expire))
            obj.close()
        else:
            self.cache[token] = f"{name}_{key}_{role}"

    def get_data(self, token):
        """

        :param token:
        :return:
        """
        res = 0
        if is_redis:
            obj = self.cache.get_obt()
            res = obj.exists(token)
            obj.close()
            if res != 0:
                res = {
                    "id": res.split("_")[1],
                    "username": res.split("_")[0],
                    "role": res.split("_")[2],
                }
        else:
            data = self.cache.get(token, 0)
            if data != 0:
                res = {"id": data.split("_")[1],
                       "username": data.split("_")[0],
                       "role": data.split("_")[2]
                       }
        return res

    def del_data(self, token):
        """
        删除缓存
        :param token:
        :return:
        """
        if is_redis:
            obj = self.cache.get_obt()
            obj.delete(token.token)
            obj.close()
        else:
            if token.token in self.cache:
                del self.cache[token.token]


catch = CatchTool()
catch.get_catch_client()
