# password_util.py
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password):
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password) -> bool:
    """
    验证明文密码是否与哈希匹配
    :param password: 明文密码
    :param hashed: 哈希密码
    :return: True 表示匹配，False 表示不匹配
    """
    
    return pwd_context.verify(plain_password, hashed_password)

