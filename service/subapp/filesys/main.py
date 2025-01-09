from fastapi import FastAPI
from .routers import files

filesys_app = FastAPI(redirect_slashes=False, title="文件管理系统")

filesys_app.include_router(files.router, prefix="/filesys", tags=["files"])

@filesys_app.get("/")
async def root():
    return {"message": "文件管理系统已启动"} 