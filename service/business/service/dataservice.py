#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/12/8 18:21
@author: nothing4any
@file: dataservice
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""
import asyncio
import datetime
import hashlib
import uuid
from abc import ABC
from urllib.parse import quote

from fastapi import UploadFile, HTTPException

from business.impl.dataImpl import Interface
from business.service.authservice import AuthService
from db.database import DataBase
from models.exec_sql.admin_sql import AdminDataRequestOperate
from models.exec_sql.state_sql import DataRequestOperate, DataHandleOperate, FileOperate, DataSignboard
from schemas import schemas
from subapp.filesys.routers.files import upload_file
from utils.logger import main_log
from fastapi.responses import FileResponse

from utils.tools import time_ago

logger = main_log


class Service(Interface, ABC):

    def __init__(self):
        super().__init__()
        self.authtool = AuthService()
        self.db = DataBase()

    async def data_request(self, item: schemas.DataReq):
        res = schemas.Out(code="400", data={}, msg="服务异常,提交失败")
        sql = DataRequestOperate.createreq.value
        req_no = "REQ" + item.reqid + datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        await self.db.init()

        req_name, handler_name = await asyncio.gather(
            self.db.execute("select real_name from admin_users where usernumber = %s"
                            , (item.reqid,)),
            self.db.execute("select real_name from admin_users where usernumber = %s"
                            , (item.handler,))
        )
        para = (req_no, item.reqid, item.handler, item.datatype, item.purpose
                , item.expectedDate, req_name[0][0], handler_name[0][0])
        sql1 = DataRequestOperate.intofields.value
        l = []
        for field in item.fields:
            l.append((req_no, field.get("name"), field.get("type"), field.get("description")))
        para1 = l

        sql2 = DataHandleOperate.insert_detail.value
        """
        (request_no, operator, remake, editstatus, file_no, title, `type`)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """
        para2 = (req_no, item.reqid, "提交请求"
                 , "pending", "", "提交请求", "提交请求")
        db_response, db_response1, db_response2 = await asyncio.gather(self.db.execute(sql, para)
                                                                       , self.db.executemany(sql1, para1)
                                                                       , self.db.execute(sql2, para2))
        if db_response != 0 and db_response1 != 0 and db_response2 != 0:
            res.code = "200"
            res.msg = "请求已提交,请等待处理"

        return res

    async def handle_request_accept(self, item: schemas.MyDataStatusEdit):
        res = schemas.Out(code="400", data={}, msg="服务异常,提交失败")
        sql = DataRequestOperate.updateedit.value
        para = (item.status, item.requestid, item.requestno)
        resdata = await self.db.execute(sql, para)
        if resdata != 0:
            res.code = "200"
            res.msg = "请求已处理"
        return res

    async def my_data_edit(self, item: schemas.MyDataEdit):
        res = schemas.Out(code="400", data={}, msg="服务异常,提交失败")
        sql = DataRequestOperate.updateedit.value
        para = (item.status, item.requestid, item.requestno)

        sql1 = DataHandleOperate.insert_detail.value
        para1 = (item.requestno, item.requestid, item.remake
                 , item.status, "", "状态变更", "状态变更")
        await self.db.init()
        db_response1, db_response = await asyncio.gather(self.db.execute(sql1, para1)
                                                         , self.db.execute(sql, para))
        if db_response1 != 0 and db_response != 0:
            res.code = "200"
            res.msg = "请求已处理"
        return res

    async def my_data_infos(self, item: schemas.DataReqInfos):
        res = schemas.Out(code="400", data={}, msg="服务异常,查询失败")
        sql = DataRequestOperate.reqlist.value
        para = (item.usernumber, int(item.pagesize) * int(item.pagenumber - 1)
                , int(item.pagesize) * int(item.pagenumber))
        # TODO admin用户逻辑
        if item.usernumber == '100001':
            sql = AdminDataRequestOperate.reqlist.value
            para = (int(item.pagesize) * int(item.pagenumber - 1)
                    , int(item.pagesize) * int(item.pagenumber))
        if item.status != "" and item.stratdt == "":
            sql = DataRequestOperate.reqlistwithstatus.value
            para = (item.usernumber, item.status, int(item.pagesize) * int(item.pagenumber - 1)
                    , int(item.pagesize) * int(item.pagenumber))
            if item.usernumber == '100001':
                sql = AdminDataRequestOperate.reqlistwithstatus.value
                para = (item.status, int(item.pagesize) * int(item.pagenumber - 1)
                        , int(item.pagesize) * int(item.pagenumber))
        if item.status != "" and item.stratdt != "":
            sql = DataRequestOperate.reqlistwithfilter.value
            para = (
                item.usernumber, item.status, item.stratdt, item.enddt, int(item.pagesize) * int(item.pagenumber - 1)
                , int(item.pagesize) * int(item.pagenumber))
        if item.status == "" and item.stratdt != "":
            sql = DataRequestOperate.reqlistwithdate.value
            para = (item.usernumber, item.stratdt, item.enddt, int(item.pagesize) * int(item.pagenumber - 1)
                    , int(item.pagesize) * int(item.pagenumber))

        await self.db.init()
        resdata = await self.db.execute(sql, para)

        l = []
        sql = DataRequestOperate.fieldslist.value
        tasks = [self.db.execute(sql, (i[0])) for i in resdata]
        results = await asyncio.gather(*tasks)
        for i in resdata:
            l.append(
                {
                    "requestId": i[0],
                    "dataType": i[3],
                    "submitDate": i[7],
                    "expectedDate": i[5],
                    "handler": i[2],
                    "status": i[6],
                    "purpose": i[4],
                    "fields": [],
                    "reqname": i[8],
                    "handlername": i[9]
                }
            )
        for i in results:
            if len(i) >= 1:
                for j in l:
                    if j.get("requestId") == i[0][0]:
                        j["fields"] = [{"name": v[1], "type": v[2], "description": v[3]} for v in i]

        if resdata != 0:
            res.code = "200"
            res.msg = "查询完成"
            res.data = l

        return res

    async def my_data_count(self, item: schemas.DataReqInfos):
        res = schemas.Out(code="400", data={}, msg="服务异常,查询失败")
        sql = DataRequestOperate.reqlistcount.value
        para = (item.usernumber,)
        if item.status != "" and item.stratdt == "":
            sql = DataRequestOperate.reqlistwithstatus_c.value
            para = (item.usernumber, item.status)
        if item.status != "" and item.stratdt != "":
            sql = DataRequestOperate.reqlistwithfilter_c.value
            para = (item.usernumber, item.status, item.stratdt, item.enddt,)
        if item.status == "" and item.stratdt != "":
            sql = DataRequestOperate.reqlistwithdate_c.value
            para = (item.usernumber, item.stratdt, item.enddt)
        await self.db.init()
        resdata = await self.db.execute(sql, para)

        if resdata != 0:
            res.code = "200"
            res.msg = "查询完成"
            res.data = resdata[0][0]

        return res

    async def handle_data_infos(self, item: schemas.DataReqInfos):
        res = schemas.Out(code="400", data={}, msg="服务异常,查询失败")
        sql = DataHandleOperate.reqlist.value
        para = (item.usernumber, int(item.pagesize) * int(item.pagenumber - 1)
                , int(item.pagesize) * int(item.pagenumber))
        if item.status != "" and item.stratdt == "":
            sql = DataHandleOperate.reqlistwithstatus.value
            para = (item.usernumber, item.status, int(item.pagesize) * int(item.pagenumber - 1)
                    , int(item.pagesize) * int(item.pagenumber))
        if item.status != "" and item.stratdt != "":
            sql = DataHandleOperate.reqlistwithfilter.value
            para = (
                item.usernumber, item.status, item.stratdt, item.enddt, int(item.pagesize) * int(item.pagenumber - 1)
                , int(item.pagesize) * int(item.pagenumber))
        if item.status == "" and item.stratdt != "":
            sql = DataHandleOperate.reqlistwithdate.value
            para = (item.usernumber, item.stratdt, item.enddt, int(item.pagesize) * int(item.pagenumber - 1)
                    , int(item.pagesize) * int(item.pagenumber))

        await self.db.init()
        resdata = await self.db.execute(sql, para)

        l = []
        sql = DataHandleOperate.fieldslist.value
        tasks = [self.db.execute(sql, (i[0])) for i in resdata]
        results = await asyncio.gather(*tasks)
        for i in resdata:
            l.append(
                {
                    "requestId": i[0],
                    "dataType": i[3],
                    "submitDate": i[7],
                    "expectedDate": i[5],
                    "handler": i[2],
                    "status": i[6],
                    "purpose": i[4],
                    "submitter": i[1],
                    "fields": [],
                    "reqname": i[8],
                    "handlername": i[9]
                }
            )
        for i in results:
            if len(i) >= 1:
                for j in l:
                    if j.get("requestId") == i[0][0]:
                        j["fields"] = [{"name": v[1], "type": v[2], "description": v[3]} for v in i]

        if resdata != 0:
            res.code = "200"
            res.msg = "查询完成"
            res.data = l

        return res

    async def handle_data_count(self, item: schemas.DataReqInfos):
        res = schemas.Out(code="400", data={}, msg="服务异常,查询失败")
        sql = DataHandleOperate.reqlistcount.value
        para = (item.usernumber,)
        if item.status != "" and item.stratdt == "":
            sql = DataHandleOperate.reqlistwithstatus_c.value
            para = (item.usernumber, item.status)
        if item.status != "" and item.stratdt != "":
            sql = DataHandleOperate.reqlistwithfilter_c.value
            para = (item.usernumber, item.status, item.stratdt, item.enddt,)
        if item.status == "" and item.stratdt != "":
            sql = DataHandleOperate.reqlistwithdate_c.value
            para = (item.usernumber, item.stratdt, item.enddt)
        await self.db.init()
        resdata = await self.db.execute(sql, para)

        if resdata != 0:
            res.code = "200"
            res.msg = "查询完成"
            res.data = resdata[0][0]

        return res

    async def handle_file_update(self, filedata: UploadFile, item: schemas.FileAndUpdate):
        res = schemas.Out(code="400", data={}, msg="服务异常,上传失败")
        # 更新数据库状态
        sql = DataHandleOperate.updateedit.value
        para = ("completed", item.usernumber, item.requestid)
        await self.db.init()
        file_response, db_response = await asyncio.gather(upload_file(filedata), self.db.execute(sql, para))
        sql1 = DataHandleOperate.insert_detail.value
        """
        (request_no, operator, remake, editstatus, file_no, title, `type`)
        VALUES(%s, %s, %s, %s, %s, %s, 'primary')
        """
        para1 = (item.requestid, item.usernumber, item.note
                 , item.status, file_response.get("fileno"), "请求处理完成", "请求处理完成")
        sql2 = FileOperate.file_submit.value
        "file_id, file_name, file_path, request_no"
        para2 = (file_response.get("fileno"), file_response.get("filename"), file_response.get("path"), item.requestid)
        resdata, resdata1 = await asyncio.gather(self.db.execute(sql1, para1), self.db.execute(sql2, para2))

        if resdata != 0 and resdata1 != 0:
            res.code = "200"
            res.msg = "处理完成"
            res.data = []

        return res

    async def process_records(self, item: schemas.ProcessRecords):
        res = schemas.Out(code="400", data={}, msg="服务异常,上传失败")
        # 更新数据库状态
        sql = DataHandleOperate.processrecords.value
        para = (item.requestno,)
        await self.db.init()
        resdata = await self.db.execute(sql, para)
        if resdata != 0:
            data = [{
                "time": d[2],
                "type": d[4],
                "title": d[3],
                "content": d[1],
                "user": d[0]
            } for d in resdata]
            res.code = "200"
            res.msg = "处理完成"
            res.data = data
        return res

    async def download(self, item: schemas.download):
        sql = FileOperate.file_list.value
        para = (item.requestno,)
        await self.db.init()
        resdata = await self.db.execute(sql, para)
        "file_id, file_name, file_path, create_dt, request_no"
        file_type = None
        file_path = None
        file_name = None
        if resdata != 0:
            file_type = resdata[0][1].split(".")[-1]
            file_path = resdata[0][2]
            file_name = resdata[0][1]
        # 根据文件类型确定文件路径和媒体类型
        if file_type == "txt":
            media_type = "text/plain"
        elif file_type == "pdf":
            media_type = "application/pdf"
        elif file_type == "jpg":
            media_type = "image/jpeg"
        elif file_type == "csv":
            media_type = "text/csv"
        elif file_type == "xlsx":
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif file_type == "xls":
            media_type = "application/vnd.ms-excel"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        if file_type is None or file_path is None:
            return None
        file_name_encoded = quote(file_name, encoding='utf-8')
        headers = {
            "Content-Disposition": f'attachment; filename="{file_name}"; filename*=UTF-8\'\'{file_name_encoded}'
        }
        return FileResponse(path=file_path, filename=file_name, media_type=media_type
                            , headers=headers)

    async def task_overview(self, item: schemas.TaskOverview):
        res = schemas.Out(code="400", data={}, msg="服务异常")
        sql = DataSignboard.task_overview.value
        para = (item.usernumber, item.usernumber, item.usernumber,)
        await self.db.init()
        resdata = await self.db.execute(sql, para)
        if resdata != 0:
            data = {
                "urgentTasks": resdata[0][0],
                "appliedTasks": resdata[1][0],
                "extractingTasks": resdata[2][0]
            }
            res.code = "200"
            res.msg = "处理完成"
            res.data = data
        return res

    async def task_overview_info(self, item: schemas.TaskOverviewInfo):
        res = schemas.Out(code="400", data={}, msg="服务异常")
        sql = DataSignboard.task_overview_info.value
        para = (item.usernumber,)
        await self.db.init()
        resdata = await self.db.execute(sql, para)
        if resdata != 0 or len(resdata) >= 1:
            data = [{
                "id": d[0],
                "name": d[1],
                "address": d[2],
                "nodeName": d[3],
                "status": d[4]
            } for d in resdata]
            res.code = "200"
            res.msg = "处理完成"
            res.data = data
        return res

    async def get_new_information(self):
        res = schemas.Out(code="400", data={}, msg="服务异常")
        sql = DataSignboard.new_information.value
        await self.db.init()
        year_start_with_time = datetime.datetime(datetime.datetime.now().year, 1, 1, 0, 0, 0)  # 添加时间 00:00:00
        year_start_str_with_time = year_start_with_time.strftime("%Y-%m-%d %H:%M:%S")
        resdata = await self.db.execute(sql, (year_start_str_with_time,))
        if resdata != 0 or len(resdata) >= 1:
            "id, info_no, title, create_dt, content, diff_time, `type`, category"
            data = [{
                "id": d[0],
                "info_no": d[1],
                "title": d[2],
                "create_dt": d[3],
                "content": d[4],
                "diff_time": d[5],
                "type": d[6],
                "category": d[7]
            } for d in resdata]
            res.code = "200"
            res.msg = "处理完成"
            res.data = data
        return res

    async def add_new_information(self, item: schemas.AddNewInformation):
        res = schemas.Out(code="400", data={}, msg="服务异常")
        sql = DataSignboard.new_information_add.value
        await self.db.init()
        "info_no, title, content, diff_time, `type`, category"
        info_no = hashlib.sha256(item.content.encode("utf-8")).hexdigest()[0:5] + "-" + str(uuid.uuid4())[0:5]
        para = (info_no, item.title, item.content, "", item.type, item.category)
        resdata = await self.db.execute(sql, para)
        if resdata != 0 or len(resdata) >= 1:
            res.code = "200"
            res.msg = "处理完成"
            res.data = []
        return res

    async def edit_new_information(self, item: schemas.AddNewInformation):
        res = schemas.Out(code="400", data={}, msg="服务异常")
        sql = DataSignboard.new_information_edit.value
        await self.db.init()
        para = (item.title, item.content, item.type, item.category, item.info_no)
        resdata = await self.db.execute(sql, para)
        if resdata != 0:
            res.code = "200"
            res.msg = "处理完成"
            res.data = []
        return res

    async def del_new_information(self, item: schemas.NewInformation):
        res = schemas.Out(code="400", data={}, msg="服务异常")
        sql = DataSignboard.new_information_del.value
        await self.db.init()
        para = (item.infono,)
        resdata = await self.db.execute(sql, para)
        if resdata != 0:
            res.code = "200"
            res.msg = "处理完成"
            res.data = []
        return res

    async def get_new_information_view(self):
        res = schemas.Out(code="400", data={}, msg="服务异常")
        sql = DataSignboard.new_information_view.value
        await self.db.init()
        resdata = await self.db.execute(sql, None)
        # datetime.datetime.strptime(d[3], "%Y-%m-%d %H:%M:%S")
        if resdata != 0 or len(resdata) >= 1:
            data = [{
                "id": d[1],
                "title": d[4] + ": " + d[2],
                "diff_time": time_ago(d[3]),
            } for d in resdata]
            res.code = "200"
            res.msg = "处理完成"
            res.data = data
        return res