"""
Created on 2024/11/30 21:33
@author: nothing4any
@file: api
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""

from abc import ABC, abstractmethod
from schemas.schemas import *


class Interface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def login(self, token: Login):
        pass

    @abstractmethod
    async def unlogin(self, token: Token):
        pass


