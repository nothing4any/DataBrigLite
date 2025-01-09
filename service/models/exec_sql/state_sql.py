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
from enum import Enum, unique


@unique
class UserOperate(Enum):
    usercreate = """
    INSERT INTO admin_users
    (usernumber, password, real_name, email, department, `role`, status)
    VALUES(%s, %s, %s, %s, %s, %s, '1');
    """

    userlist = """
    select usernumber, real_name, role, created_at, email, department, status from admin_users
    limit {}, {};
    """

    usersearchone = """
    select count(1) from 
    admin_users where usernumber = %s and status = '1';
    """

    usersearch = """
    select id, real_name, password, `role`, usernumber from 
    admin_users where usernumber = '{}' and status = '1';
    """

    updtaepasswd = """
    update admin_users set password = "{}" where usernumber = '{}' and status = '1';
    """


@unique
class DataRequestOperate(Enum):
    createreq = """
    INSERT INTO dataplatform.data_requests
    (request_no, requester_id, handler_id, data_type, purpose
    , expected_date, status, requester_name, handler_name)
    VALUES(%s, %s, %s, %s, %s, %s, 'pending', %s, %s);
    """

    reqlist = """
    SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date
    , status, created_at, requester_name, handler_name
    FROM dataplatform.data_requests where requester_id = %s limit %s, %s ;
    """

    reqlistcount = """
    SELECT count(*)
    FROM dataplatform.data_requests where requester_id = %s;
    """

    reqlistwithstatus = """
    SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date
    , status, created_at, requester_name, handler_name
    FROM dataplatform.data_requests where requester_id = %s and status = %s limit %s, %s ;
    """

    reqlistwithstatus_c = """
    SELECT count(*)
    FROM dataplatform.data_requests where requester_id = %s and status = %s;
    """

    reqlistwithdate = """
    SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date
    , status, created_at, requester_name, handler_name
    FROM dataplatform.data_requests where requester_id = %s and created_at >= %s and created_at < %s limit %s, %s ;
    """

    reqlistwithdate_c = """
    SELECT count(*)
    FROM dataplatform.data_requests where requester_id = %s and created_at >= %s and created_at < %s;
    """

    reqlistwithfilter = """
    SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date
    , status, created_at, requester_name, handler_name
    FROM dataplatform.data_requests 
    where requester_id = %s
    and status = %s
    and created_at >= %s 
    and created_at < %s 
    limit %s, %s ;
    """

    reqlistwithfilter_c = """
    SELECT count(*)
    FROM dataplatform.data_requests 
    where requester_id = %s
    and status = %s
    and created_at >= %s 
    and created_at < %s;
    """

    updateedit = """
    update dataplatform.data_requests set status = %s
    where requester_id = %s and request_no = %s;
    """

    intofields = """
    INSERT INTO dataplatform.request_fields
    (request_no, field_name, field_type, description)
    VALUES(%s, %s, %s, %s);
    """

    fieldslist = """
    SELECT request_no, field_name, field_type, description
    FROM dataplatform.request_fields
    where request_no = %s ;
    """


@unique
class DataHandleOperate(Enum):
    data_hadnnle_detail = """
    INSERT INTO dataplatform.requests_handle_detail
    (request_no, handler_id, remake, editstatus, file_no)
    VALUES(%s, %s, %s, %s, %s);
    """

    update_status = """
    update update dataplatform.requests_handle_detail 
    set editstatus = %s, 
    where requester_id = %s and request_no = %s;
    """

    update_with_remake = """
    update update dataplatform.requests_handle_detail 
    set editstatus = %s, remake = %s
    where requester_id = %s and request_no = %s;
    """

    update_file = """
    update update dataplatform.requests_handle_detail 
    set file_no = %s, 
    where requester_id = %s and request_no = %s;
    """

    reqlist = """
        SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date
        , status, created_at, requester_name, handler_name
        FROM dataplatform.data_requests where handler_id = %s limit %s, %s ;
        """

    reqlistcount = """
        SELECT count(*)
        FROM dataplatform.data_requests where handler_id = %s;
        """

    reqlistwithstatus = """
        SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date
        , status, created_at, requester_name, handler_name
        FROM dataplatform.data_requests where handler_id = %s and status = %s limit %s, %s ;
        """

    reqlistwithstatus_c = """
        SELECT count(*)
        FROM dataplatform.data_requests where handler_id = %s and status = %s;
        """

    reqlistwithdate = """
        SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date
        , status, created_at, requester_name, handler_name
        FROM dataplatform.data_requests where handler_id = %s and created_at >= %s and created_at < %s limit %s, %s ;
        """

    reqlistwithdate_c = """
        SELECT count(*)
        FROM dataplatform.data_requests where handler_id = %s and created_at >= %s and created_at < %s;
        """

    reqlistwithfilter = """
        SELECT request_no, requester_id, handler_id, data_type, purpose, expected_date
        , status, created_at, requester_name, handler_name
        FROM dataplatform.data_requests 
        where handler_id = %s
        and status = %s
        and created_at >= %s 
        and created_at < %s 
        limit %s, %s ;
        """

    reqlistwithfilter_c = """
        SELECT count(*)
        FROM dataplatform.data_requests 
        where handler_id = %s
        and status = %s
        and created_at >= %s 
        and created_at < %s;
        """

    updateedit = """
        update dataplatform.data_requests set status = %s
        where handler_id = %s and request_no = %s;
        """

    fieldslist = """
        SELECT request_no, field_name, field_type, description
        FROM dataplatform.request_fields
        where request_no = %s ;
        """

    insert_detail = """
    INSERT INTO dataplatform.requests_handle_detail
    (request_no, operator, remake, editstatus, file_no, title, `type`)
    VALUES(%s, %s, %s, %s, %s, %s, %s);
    """

    processrecords = """
    SELECT t2.real_name, t1.remake, t1.created_at, t1.title, t1.`type`
    FROM dataplatform.requests_handle_detail t1
    left join dataplatform.admin_users t2
    on t1.operator = t2.usernumber
    where request_no = %s order by created_at desc;
    """

@unique
class FileOperate(Enum):
    file_list = """
    SELECT file_id, file_name, file_path, create_dt, request_no
    FROM dataplatform.request_files where request_no = %s 
    ORDER BY create_dt DESC limit 1;
    """

    file_submit = """
    INSERT INTO dataplatform.request_files
    (file_id, file_name, file_path, request_no)
    VALUES(%s, %s, %s, %s);
    """

@unique
class DataSignboard(Enum):
    new_information = """
    SELECT id, info_no, title, create_dt, content, diff_time, `type`, category
    FROM dataplatform.notices_infos
    where create_dt > STR_TO_DATE(%s, '%%Y-%%m-%%d %%H:%%i:%%s')
    ;
    """
    new_information_add = """
    INSERT INTO dataplatform.notices_infos
    (info_no, title, content, diff_time, `type`, category)
    VALUES(%s, %s, %s, %s, %s, %s);
    """

    new_information_edit = """
    UPDATE dataplatform.notices_infos
    SET title=%s, content=%s, `type`=%s, category=%s
    WHERE info_no=%s;
    """

    new_information_del = """
    DELETE FROM dataplatform.notices_infos
    WHERE info_no = %s;
    """

    new_information_view = """
    SELECT id, info_no, title, create_dt, category
    FROM dataplatform.notices_infos
    order by create_dt
    limit 5
    ;
    """

    task_overview = """
    SELECT count(*) as task_count
    FROM dataplatform.data_requests
    where handler_id = %s and status = 'completed'
    union all
    SELECT count(*) as task_count
    FROM dataplatform.data_requests
    where handler_id = %s and status = 'processing'
    union all
    SELECT count(*) as task_count
    FROM dataplatform.data_requests
    where handler_id = %s and status = 'pending'
    ;
    """

    task_overview_info = """
    SELECT
        t1.id as id
        ,t3.real_name as name
        ,t4.dict_key as address
        ,t2.dict_key as nodename
        ,t1.status as status
    FROM
        dataplatform.data_requests t1
    left join dataplatform.dict_items t2
    on
        t1.status = t2.dict_value
        and t2.dict_type = '处理状态'
    left join dataplatform.admin_users t3
    on
        t1.requester_id = t3.usernumber
    left join dataplatform.dict_items t4
    on
        t3.department = t4.dict_value
        and t4.dict_type = '部门'
    where
        t1.handler_id = %s
    and t1.status <> 'completed'
    ;
    """