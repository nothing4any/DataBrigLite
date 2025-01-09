"""
Created on 2024/11/30 21:33
@author: nothing4any
@file: user
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""

from abc import ABC, abstractmethod

from schemas import schemas


class Interface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def user_create(self, item: schemas.UserCreate):
        pass

    @abstractmethod
    def user_list(self, item: schemas.UserSearch):
        pass

    @abstractmethod
    def user_update(self, item: schemas.UserUpdate):
        pass

    @abstractmethod
    def user_delete(self, item: schemas.UserDelete):
        pass

    @abstractmethod
    def user_status(self, item: schemas.UserStatus):
        pass

    @abstractmethod
    def user_map_req(self):
        pass
