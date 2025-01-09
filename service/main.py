import asyncio
import os
import sys
import time

from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from middleware.auth import AuthMiddleware, RequestLogger

sys.path.append(".")
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import api, user, data

from models import models
from utils.logger import setup_logger
from core.catchdata import catch
from subapp.filesys.main import filesys_app

# 创建日志记录器
logger = setup_logger("main")

models.create_all()

app = FastAPI(
    # 禁用自动追加尾部斜杠
    redirect_slashes=False
)
app.mount("/file", filesys_app)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 添加中间件记录请求日志
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     duration = time.time() - start_time
#
#     logger.info(
#         f"Method: {request.method} Path: {request.url.path} "
#         f"Status: {response.status_code} Duration: {duration:.2f}s"
#     )
#
#     return response


# 添加中间件
# app.add_middleware(AuthMiddleware)
app.add_middleware(RequestLogger)


# 挂载路由
app.include_router(api.router, prefix="/api")
app.include_router(user.router, prefix="/api/user")
app.include_router(data.router, prefix="/api/data")


# 静态文件位置
static_dir = os.path.dirname(os.path.abspath(__file__))
parten = os.path.dirname(static_dir)

# ##接口文档
app.mount("/static", StaticFiles(directory=f"{static_dir}/static/doc"), name="static_web")

# ui
app.mount("/ui", StaticFiles(directory=f"{static_dir}/static/ui/dist"), name="static_ui")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/doc/swagger-ui-bundle.js",
        swagger_css_url="/static/doc/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.get("/")
def read_root():
    html_path = f"{static_dir}/static/ui/dist/index.html"
    html_content = ''
    with open(html_path, encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5001)
