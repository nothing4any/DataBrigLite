import hashlib

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse

import os
from datetime import datetime
from ..config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
import uuid

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile):
    # 检查文件扩展名
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    # 保存文件
    try:
        # contents: bytes = await file.read()
        # if len(contents) > MAX_FILE_SIZE:
        #     raise HTTPException(status_code=400, detail="文件大小超过限制")
        total_size = 0
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)  # 每次读取1KB
                if not chunk:
                    break
                buffer.write(chunk)
                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=400, detail="文件大小超过限制")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")
    file_no = "".join(unique_filename.split(".")[0:-1]) + datetime.now().strftime("%Y%m%d%H%M%S") + "-" + \
              hashlib.sha256(unique_filename.encode("utf-8")).hexdigest()[0:5] + "-" + str(uuid.uuid4())[0:5]
    return {"fileno": file_no, "filename": unique_filename, "path": str(file_path)}


@router.get("/files/")
async def list_files():
    files = []
    for file in UPLOAD_DIR.glob("*"):
        if file.is_file():
            files.append({
                "filename": file.name,
                "size": file.stat().st_size,
                "created_at": datetime.fromtimestamp(file.stat().st_ctime).isoformat()
            })
    return files


@router.get("/files/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(path=file_path, filename=filename)


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")
    return {"message": "文件删除成功"}
