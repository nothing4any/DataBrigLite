#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2024/12/1 10:51
@author: nothing4any
@file: auth
@Project: dataplatform-server
@Software: PyCharm
@Description:
"""
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import json

from starlette.types import Message

from core.catchdata import catch
from utils.logger import main_log


# TODO 路由拦截


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # 登录路由不需要验证
            if "/login" in request.url.path:
                return await call_next(request)

            # 验证 token
            token = request.headers.get("Authorization")
            if not token:
                return Response(
                    content=json.dumps({"code": "401", "message": "未提供认证令牌"}),
                    status_code=401,
                    media_type="application/json"
                )

            token = token.split(" ")[1]  # 去掉 "Bearer " 前缀
            try:
                userdata = catch.get_data(token)
                # if userdata != 0 and request.path_params
                if userdata == 0:
                    if "/unlogin" in request.url.path:
                        return await call_next(request)
                    main_log.error(f"无效的token: {token}")
                    return Response(
                        content=json.dumps({"code": "401", "message": "无效的认证令牌"}),
                        status_code=401,
                        media_type="application/json"
                    )
                return await call_next(request)
            except Exception as e:
                main_log.error(f"服务异常 {e}")
                return Response(
                    content=json.dumps({"code": "500", "message": "服务异常"}),
                    status_code=500,
                    media_type="application/json"
                )

        except Exception as e:
            main_log.error(f"中间件处理异常: {e}")
            return Response(
                content=json.dumps({"code": "500", "message": "服务器内部错误"}),
                status_code=500,
                media_type="application/json"
            )


class RequestLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 获取请求路径
        path = request.url.path
        # 获取客户端 IP
        client_ip = request.client.host

        # 获取请求参数
        params = {}
        # 获取查询参数
        query_params = dict(request.query_params)
        if query_params:
            params['query_params'] = query_params

        # 创建一个接收请求体的新方法
        async def set_body(request: Request):
            receive_ = await request._receive()

            async def receive():
                return receive_

            request._receive = receive

        await set_body(request)
        # 获取 JSON 请求体
        if request.headers.get('content-type') == 'application/json':
            try:
                body = await request.body()
                if body:
                    json_body = json.loads(body)
                    params['json_body'] = json_body
            except:
                params['json_body'] = None

        log_data = {
            'path': path,
            'client_ip': client_ip,
            'params': params,
            'method': request.method
        }

        main_log.info(f"Request info: {json.dumps(log_data, ensure_ascii=False)}")

        start_time = time.time()
        # 继续处理请求
        response = await call_next(request)
        duration = time.time() - start_time

        main_log.info(f"Method: {request.method} Path: {request.url.path} ")
        main_log.info(f"Status: {response.status_code} Duration: {duration:.2f}s")

        return response
