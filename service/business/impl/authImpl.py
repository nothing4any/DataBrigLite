#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/11/30 21:50
@author: nothing4any
@file: auth
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from schemas.schemas import User


class Interface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str):
        pass

    @abstractmethod
    def get_password_hash(self, password: str):
        pass

    @abstractmethod
    def get_current_active_user(self, current_user: User):
        pass

    @abstractmethod
    def get_current_admin_user(self):
        pass
