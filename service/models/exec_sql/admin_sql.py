#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/12/31 下午10:59
@file: admin_sql
@author: nothing4any
Description:
"""
from enum import Enum, unique


@unique
class AdminDataRequestOperate(Enum):

    reqlist = """
    SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date, status, created_at
    FROM dataplatform.data_requests limit %s, %s ;
    """

    reqlistcount = """
    SELECT count(*)
    FROM dataplatform.data_requests ;
    """

    reqlistwithstatus = """
    SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date, status, created_at
    FROM dataplatform.data_requests where status = %s limit %s, %s ;
    """

    reqlistwithstatus_c = """
    SELECT count(*)
    FROM dataplatform.data_requests where  status = %s;
    """

    reqlistwithdate = """
    SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date, status, created_at
    FROM dataplatform.data_requests where created_at >= %s and created_at < %s limit %s, %s ;
    """

    reqlistwithdate_c = """
    SELECT count(*)
    FROM dataplatform.data_requests where  created_at >= %s and created_at < %s;
    """

    reqlistwithfilter = """
    SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date, status, created_at
    FROM dataplatform.data_requests 
    where status = %s
    and created_at >= %s 
    and created_at < %s 
    limit %s, %s ;
    """

    reqlistwithfilter_c = """
    SELECT count(*)
    FROM dataplatform.data_requests 
    where status = %s
    and created_at >= %s 
    and created_at < %s;
    """

    fieldslist = """
    SELECT request_no, field_name, field_type, description
    FROM dataplatform.request_fields
    where request_no = %s ;
    """


@unique
class AdminDataHandleOperate(Enum):

    reqlist = """
        SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date, status, created_at
        FROM dataplatform.data_requests where handler_id = %s limit %s, %s ;
        """

    reqlistcount = """
        SELECT count(*)
        FROM dataplatform.data_requests where handler_id = %s;
        """

    reqlistwithstatus = """
        SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date, status, created_at
        FROM dataplatform.data_requests where handler_id = %s and status = %s limit %s, %s ;
        """

    reqlistwithstatus_c = """
        SELECT count(*)
        FROM dataplatform.data_requests where handler_id = %s and status = %s;
        """

    reqlistwithdate = """
        SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date, status, created_at
        FROM dataplatform.data_requests where handler_id = %s and created_at >= %s and created_at < %s limit %s, %s ;
        """

    reqlistwithdate_c = """
        SELECT count(*)
        FROM dataplatform.data_requests where handler_id = %s and created_at >= %s and created_at < %s;
        """

    reqlistwithfilter = """
        SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date, status, created_at
        FROM dataplatform.data_requests 
        where status = %s
        and created_at >= %s 
        and created_at < %s 
        limit %s, %s ;
        """

    reqlistwithfilter_c = """
        SELECT count(*)
        FROM dataplatform.data_requests 
        where status = %s
        and created_at >= %s 
        and created_at < %s;
        """

    fieldslist = """
        SELECT request_no, field_name, field_type, description
        FROM dataplatform.request_fields
        where request_no = %s ;
        """


@unique
class AdminFileOperate(Enum):
    file_list = """
    SELECT file_id, file_name, file_path, create_dt, request_no
    FROM dataplatform.request_files where request_no = %s 
    DESC create_dt limit 1;
    """

