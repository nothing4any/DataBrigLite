#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/12/1 20:19
@author: nothing4any
@file: authservice
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""
from abc import ABC
from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException

from jose import jwt, JWTError

from core.security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, pwd_context, oauth2_scheme
from core.catchdata import catch
from business.impl.authImpl import Interface
from schemas.schemas import *
from fastapi import status

from utils.logger import main_log

logger = main_log


class AuthService(Interface, ABC):

    def __init__(self):
        super().__init__()
        self.logger = logger

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_password_hash(self, password: str):
        """
        对密码进行哈希加密
        """
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        :param plain_password: 明文密码
        :param hashed_password: 哈希后的密码
        :return: 验证是否通过
        """
        return pwd_context.verify(plain_password, hashed_password)

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        userres = None
        user = None
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")
            if username is None:
                raise credentials_exception
            userres = catch.get_data(token)
            if userres == 0:
                self.logger.error("用户未登录")
                self.logger.error(f"尝试的token: {token}")
        except JWTError:
            self.logger.error("token解析异常")
            self.logger.error(f"尝试的token: {token}")
        if userres is not None:
            user = User(**userres)
        if user is None:
            self.logger.error("用户未登录")
            self.logger.error(f"尝试的token: {token}")
        return user

    async def get_current_active_user(self, current_user: User = Depends(get_current_user)):
        if "user" not in current_user.role:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    async def get_current_admin_user(self, current_user: User = Depends(get_current_user)):
        if "admin" not in current_user.role:
            raise HTTPException(status_code=400, detail="User is not an admin")
        return current_user

# if __name__ == '__main__':
#     print(pwd_context.hash("admin"))
    # from core.catchdata import CatchTool
    # catch = CatchTool()
    # catch.get_catch_client()
    #
    # async def main():
    #     data = {"username": "johndoe", "id": "123", "role": "admin"}
    #     s = Service()
    #     s1 = await s.create_access_token(data)
    #     catch.set_data(s1, "johndie", "123", "admin", None)
    #     print(s1)
    #     s2 = await s.get_current_user(s1)
    #     print(s2)
    #
    #
    # import asyncio
    #
    # asyncio.run(main())
