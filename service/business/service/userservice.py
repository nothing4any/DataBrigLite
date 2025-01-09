#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/12/7 21:50
@author: nothing4any
@file: userservice
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""
import datetime
import time
from abc import ABC

from db.database import DataBase
from models.exec_sql.state_sql import UserOperate
from business.impl.userImpl import Interface
from business.service.authservice import AuthService
from schemas.schemas import UserCreate, UserSearch, UserUpdate, Out, UserStatus, UserDelete
from utils.DataBaseId import getId
from utils.logger import user_log

logger = user_log


class Service(Interface, ABC):

    def __init__(self):
        super().__init__()
        self.authtool = AuthService()
        self.db = DataBase()

    async def user_create(self, item: UserCreate):
        res = Out(code="400", data={}, msg="用户创建失败,请重试")
        now = datetime.datetime.now()
        create_dt = now.strftime("%Y-%m-%d %H:%M:%S")
        id = await getId(time.time())
        await self.db.init()
        sql = UserOperate.usersearchone.value
        para = (item.usernumber,)
        resdata = await self.db.execute(sql, para)
        if resdata[0][0] >= 1:
            user_log.info("{} 用户已存在".format(item.usernumber))
            res.msg = "用户已存在,请检查用户号"
            return res
        sql = UserOperate.usercreate.value
        para = (item.usernumber, self.authtool.get_password_hash(item.password), item.username, "", item.department, item.role)
        resdata = await self.db.execute(sql, para)
        if resdata != 0:
            res.code = "200"
            res.msg = "用户创建成功"
        return res

    async def user_list(self, item: UserSearch):
        res = Out(code="400", data={}, msg="用户列表查询失败")
        await self.db.init()
        sql = UserOperate.userlist.value.format(int(item.pagesize) * int(item.pagenumber - 1)
                                                , int(item.pagesize) * int(item.pagenumber))
        resdata = await self.db.execute(sql)
        if resdata == 0 or len(resdata) == 0:
            logger.error("用户不存在或数据库服务失效")
        else:
            data = [{
                "userId": d[0],
                "username": d[1],
                "role": d[2],
                "createTime": d[3],
                "email": d[4],
                "department": d[5],
                "status": d[6]
            } for d in resdata]
            res.code = "200"
            res.data = data
            res.msg = "查询完成"

        return res

    async def user_map_req(self):
        res = Out(code="400", data={}, msg="用户查询失败")
        await self.db.init()
        sql = """
        select usernumber, real_name
        from admin_users where status = '1'
        and role = 'dataProcessor';
        """
        resdata = await self.db.execute(sql)
        if resdata == 0 or len(resdata) == 0:
            logger.error("用户不存在或数据库服务失效")
        else:
            data = [{
                "id": d[0],
                "name": d[1],
            } for d in resdata]
            res.code = "200"
            res.data = data
            res.msg = "查询完成"

        return res

    async def user_update(self, item: UserUpdate):
        res = Out(code="400", data={}, msg="用户信息更新失败,请重试")
        await self.db.init()
        sql = UserOperate.updtaepasswd.value.format(self.authtool.get_password_hash(item.password), item.usernumber)
        resdata = await self.db.execute(sql)
        if resdata != 0:
            res.code = '200'
            res.msg = "密码已变更"
        return res

    async def user_delete(self, item: UserDelete):
        pass

    async def user_status(self, item: UserStatus):
        pass