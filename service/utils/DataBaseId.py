#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/12/8 12:48
@author: nothing4any
@file: DataBaseId
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""
import requests


async def getId(sequenceId):
    data = {"machineId": 1
        , "datacenterId": 1
        , "sequenceId": sequenceId
            }
    res = requests.post(url='http://hostname:port/getDatabaseId', json=data)
    return res.json()["databaseId"]
