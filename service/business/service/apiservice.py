"""
Created on 2024/11/30 21:33
@author: nothing4any
@file: apiservice
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""
from abc import ABC

from business.impl.apiImpl import Interface
from schemas.schemas import *
from models.exec_sql.state_sql import UserOperate
from db.database import DataBase
from utils.logger import api_log
from business.service.authservice import AuthService
from core.catchdata import catch

logger = api_log


class Service(Interface, ABC):

    def __init__(self):
        super().__init__()
        self.authtool = AuthService()
        self.db = DataBase()
        self.catch = catch

    async def login(self, login: Login):
        await self.db.init()
        logger.info("登录用户信息: {}".format(login.model_dump_json()))
        res = Out(code="400", data={}, msg="用户不存在")
        userid = login.usernumber
        sql = UserOperate.usersearch.value.format(userid)
        resdata = await self.db.execute(sql, None)
        if resdata == 0 or len(resdata) == 0:
            logger.info("用户{}不存在".format(userid))
            return res
        if self.authtool.verify_password(login.password, resdata[0][2]):
            res.code = "200"
            res.msg = "登录成功"
            token = self.authtool.create_access_token({"username": resdata[0][1],
                                                       "id": resdata[0][4],
                                                       "role": resdata[0][3]})
            res.data = {"token": token, "username": resdata[0][1], "role": resdata[0][3]}
            catch.set_data(token, resdata[0][1], resdata[0][4], resdata[0][3])
        else:
            res.msg = "工号或密码错误"
        return res

    async def unlogin(self, item: Token):
        res = Out(code="400", data={}, msg="请求异常,刷新重试")
        try:
            if item is not None:
                catch.del_data(token=item)
                res.code = "200"
                res.msg = "已退出,自动返回登录界面"
            else:
                logger.error("token 不存在")
        except ValueError as e:
            logger.error(f"注销异常 {e}")
        return res
