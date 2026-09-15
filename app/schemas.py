# API接收什么数据、返回什么数据。
from datetime import datetime

from pydantic import BaseModel, ConfigDict

# 创建用户时，客户端应该传什么。
class UserCreate(BaseModel):
    username: str
    email: str

# FastAPI最后返回给用户什么。
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # Pydantic允许从一个Python对象的属性里读取数据。

# 文档的传输格式
class DocumentCreate(BaseModel):
    user_id: int
    filename: str

class DocumentResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)