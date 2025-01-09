from enum import Enum

from core.config import settings
from db.database import DataBase


async def create_all():
    if settings.IS_CREATE_TABLE:
        sqlconn = DataBase()
        await sqlconn.init()
        try:
            await sqlconn.execute(TablesInfo.admin_users.name, None)
            await sqlconn.execute(TablesInfo.data_handle.name, None)
            await sqlconn.execute(TablesInfo.file_sys_info.name, None)
        except Exception as e:
            raise Exception("数据库初始化失败")


class TablesInfo(Enum):
    admin_users = """
    CREATE TABLE admin_users (
            id int NOT NULL, 
            username VARCHAR(50), 
            role VARCHAR(50), 
            hashed_password VARCHAR(50), 
            user_number INTEGER not null,
            is_active VARCHAR(10), 
            created_at long, 
            PRIMARY KEY (id, user_number)
        );
    """

    data_handle = """
    CREATE TABLE data_handle (
            id INTEGER NOT NULL, 
            user_number VARCHAR ,
            username VARCHAR, 
            role VARCHAR, 
            hashed_password VARCHAR, 
            user_number INTEGER not null,
            is_active BOOLEAN, 
            created_at long, 
            PRIMARY KEY (id)
        );
    """

    file_sys_info = """
        CREATE TABLE data_handle (
                id INTEGER NOT NULL, 
                filename VARCHAR, 
                filepath VARCHAR, 
                user_number VARCHAR,
                created_at long, 
                PRIMARY KEY (id)
            );
        """
