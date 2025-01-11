**此文件介绍python项目配置文件的使用方法**


# 配置文件

## 配置文件使用原生python文件

## 配置文件路径：.service/core/config.py

### 数据库配置 - 使用 mysql

- DBIP: str = "hostname"
- DBPORT: str = "port"
- DBUSER: str = "user"
- DBPWD: str = "password"
- DBDATABASE: str = "database"
- DBMINSIZE: int = 100
- DBMAXSIZE: int = 300

### 日志配置
- LOG_LEVEL: str = "INFO"
- LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
- LOG_DIR: str = "logs"
- LOG_RETENTION_DAYS: int = 30

### redis
- REDISIP: str = "hostname"
- REDISPORT: str = "port"
- REDISPWD: str = "password"

### create tables
- IS_CREATE_TABLE: bool = False
