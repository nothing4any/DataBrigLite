import os
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    # 文档类型
    '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.ppt', '.pptx',
    # 图片类型
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg',
    # 压缩文件
    '.zip', '.rar', '.7z', '.tar', '.gz',
    # 音视频文件
    '.mp3', '.mp4', '.wav', '.avi', '.mov', '.wmv',
    # 开发相关
    '.json', '.xml', '.yaml', '.yml', '.md',
    # 其他常用格式
    '.html', '.htm', '.css', '.js'
}

# 最大文件大小（以字节为单位）：默认 50MB
MAX_FILE_SIZE = 50 * 1024 * 1024