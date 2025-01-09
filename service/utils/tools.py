#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/11/30 21:33
@author: nothing4any
@file: data
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""

import uuid
import hashlib
from datetime import datetime, timedelta


def file_checksum(filename, hash_factory=hashlib.sha256, chunk_num_blocks=128):
    """计算文件的哈希值，使用分块读取方式以节省内存"""
    h = hash_factory()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_num_blocks * h.block_size)
            if not chunk:  # 如果没有读到数据，说明已经读取完毕
                break
            h.update(chunk)
    return h.hexdigest()


def generate_unique_file_id(file_path):
    """
    根据文件内容和UUID生成一个唯一的文件标识符。

    参数:
    file_path (str): 文件的路径。

    返回:
    str: 文件的唯一标识符。
    """
    # 生成一个随机的UUID作为一部分唯一标识符
    random_uuid = uuid.uuid4()

    # 计算文件内容的SHA-256哈希值
    content_hash = file_checksum(file_path)

    # 将UUID和内容哈希组合成最终的唯一标识符
    unique_file_id = f"{random_uuid}-{content_hash}"

    return unique_file_id


def time_ago(dt: datetime):
    """
    接受一个 datetime 对象 dt 并返回一个字符串，
    表示 dt 与当前时间的差值为多少分钟前、多少小时前或多少天前。
    """
    if not isinstance(dt, datetime):
        raise TypeError("dt should be a datetime object")

    now = datetime.now()
    diff = now - dt

    # 计算总秒数，用于更精确的时间间隔计算
    total_seconds = int(diff.total_seconds())

    # 计算不同单位的时间间隔
    seconds = abs(total_seconds)
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    # 根据不同的时间间隔范围，返回适当的描述
    if seconds < 60:
        return f"{seconds}秒前" if seconds > 0 else "刚刚"
    elif minutes < 60:
        return f"{minutes}分钟前"
    elif hours < 24:
        return f"{hours}小时前"
    else:
        return f"{days}天前"
