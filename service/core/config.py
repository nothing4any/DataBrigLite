from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 获取项目根目录
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # 数据库配置 - 使用 mysql
    DBIP: str = "hostname"
    DBPORT: str = "port"
    DBUSER: str = "user"
    DBPWD: str = "password"
    DBDATABASE: str = "database"
    DBMINSIZE: int = 100
    DBMAXSIZE: int = 300

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DIR: str = "logs"
    LOG_RETENTION_DAYS: int = 30

    # redis
    IS_REDIS: bool = False
    REDISIP: str = "hostname"
    REDISPORT: str = "port"
    REDISPWD: str = "password"

    # create tables
    IS_CREATE_TABLE: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
