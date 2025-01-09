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

from abc import ABC, abstractmethod

from fastapi import UploadFile

from schemas import schemas


class Interface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def data_request(self, item: schemas.Login):
        """
        发起数据申请
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def my_data_infos(self, item: schemas.DataReqInfos):
        """
        查询我的申请
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def my_data_count(self, item: schemas.DataReqInfos):
        """
        查询我的申请总数
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def my_data_edit(self, item: schemas.MyDataEdit):
        """
        业务人员修改申请状态
        :param item:
        :return:
        """
        pass

    ########################################数据处理人员相关接口#######################################################
    @abstractmethod
    def handle_request_accept(self, item: schemas.MyDataStatusEdit):
        """
        数据处理人员变更申请状态
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def handle_data_infos(self, item: schemas.DataReqInfos):
        """
        查询我的申请
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def handle_data_count(self, item: schemas.DataReqInfos):
        """
        数据人员查询总条数
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def handle_file_update(self, filedata: UploadFile, item: schemas.FileAndUpdate):
        """
        接收文件，更新状态
        :param filedata:
        :param para:
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def process_records(self, item: schemas.ProcessRecords):
        """
        获取历史记录
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def download(self, item: schemas.download):
        """
        文件下载
        :param item:
        :param download:
        :return:
        """
        pass

    @abstractmethod
    def task_overview(self, item: schemas.TaskOverview):
        """
        任务概览
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def task_overview_info(self, item: schemas.TaskOverviewInfo):
        """
        任务概览-进度
        :param item:
        :return:
        """
        pass

    @abstractmethod
    def get_new_information(self):
        """
        获取通知
        :return:
        """
        pass

    @abstractmethod
    def add_new_information(self, item: schemas.AddNewInformation):
        """
        添加通知
        :return:
        """
        pass

    @abstractmethod
    def edit_new_information(self, item: schemas.AddNewInformation):
        """
        修改通知
        :return:
        """
        pass

    @abstractmethod
    def del_new_information(self, item: schemas.NewInformation):
        """
        修改通知
        :return:
        """
        pass

    @abstractmethod
    def get_new_information_view(self):
        """
        通知概览
        :return:
        """
        pass
