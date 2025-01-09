from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# JWT 密钥和算法
SECRET_KEY = "950322"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
